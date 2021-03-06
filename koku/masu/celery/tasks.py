#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Asynchronous tasks."""
import math
import os
from datetime import datetime
from datetime import timedelta

from botocore.exceptions import ClientError
from celery.exceptions import MaxRetriesExceededError
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from api.dataexport.models import DataExportRequest
from api.dataexport.syncer import AwsS3Syncer
from api.dataexport.syncer import SyncedFileInColdStorageError
from api.iam.models import Tenant
from api.models import Provider
from api.utils import DateHelper
from koku.celery import app
from masu.config import Config
from masu.database.report_manifest_db_accessor import ReportManifestDBAccessor
from masu.external.accounts.hierarchy.aws.aws_org_unit_crawler import AWSOrgUnitCrawler
from masu.external.date_accessor import DateAccessor
from masu.processor.orchestrator import Orchestrator
from masu.processor.tasks import autovacuum_tune_schema
from masu.processor.tasks import vacuum_schema
from masu.util.aws.common import get_s3_resource

LOG = get_task_logger(__name__)
_DB_FETCH_BATCH_SIZE = 2000


@app.task(name="masu.celery.tasks.check_report_updates")
def check_report_updates(*args, **kwargs):
    """Scheduled task to initiate scanning process on a regular interval."""
    orchestrator = Orchestrator(*args, **kwargs)
    orchestrator.prepare()


@app.task(name="masu.celery.tasks.remove_expired_data")
def remove_expired_data(simulate=False, line_items_only=False):
    """Scheduled task to initiate a job to remove expired report data."""
    today = DateAccessor().today()
    LOG.info("Removing expired data at %s", str(today))
    orchestrator = Orchestrator()
    orchestrator.remove_expired_report_data(simulate, line_items_only)


def deleted_archived_with_prefix(s3_bucket_name, prefix):
    """
    Delete data from archive with given prefix.

    Args:
        s3_bucket_name (str): The s3 bucket name
        prefix (str): The prefix for deletion
    """
    s3_resource = get_s3_resource()
    s3_bucket = s3_resource.Bucket(s3_bucket_name)
    object_keys = [{"Key": s3_object.key} for s3_object in s3_bucket.objects.filter(Prefix=prefix)]
    batch_size = 1000  # AWS S3 delete API limits to 1000 objects per request.
    for batch_number in range(math.ceil(len(object_keys) / batch_size)):
        batch_start = batch_size * batch_number
        batch_end = batch_start + batch_size
        object_keys_batch = object_keys[batch_start:batch_end]
        s3_bucket.delete_objects(Delete={"Objects": object_keys_batch})

    remaining_objects = list(s3_bucket.objects.filter(Prefix=prefix))
    if remaining_objects:
        LOG.warning(
            "Found %s objects after attempting to delete all objects with prefix %s", len(remaining_objects), prefix
        )


@app.task(
    name="masu.celery.tasks.delete_archived_data",
    queue_name="delete_archived_data",
    autoretry_for=(ClientError,),
    max_retries=10,
    retry_backoff=10,
)
def delete_archived_data(schema_name, provider_type, provider_uuid):
    """
    Delete archived data from our S3 bucket for a given provider.

    This function chiefly follows the deletion of a provider.

    This task is defined to attempt up to 10 retries using exponential backoff
    starting with a 10-second delay. This is intended to allow graceful handling
    of temporary AWS S3 connectivity issues because it is relatively important
    for us to delete this archived data.

    Args:
        schema_name (str): Koku user account (schema) name.
        provider_type (str): Koku backend provider type identifier.
        provider_uuid (UUID): Koku backend provider UUID.

    """
    if not schema_name or not provider_type or not provider_uuid:
        # Sanity-check all of these inputs in case somehow any receives an
        # empty value such as None or '' because we need to minimize the risk
        # of deleting unrelated files from our S3 bucket.
        messages = []
        if not schema_name:
            message = "missing required argument: schema_name"
            LOG.error(message)
            messages.append(message)
        if not provider_type:
            message = "missing required argument: provider_type"
            LOG.error(message)
            messages.append(message)
        if not provider_uuid:
            message = "missing required argument: provider_uuid"
            LOG.error(message)
            messages.append(message)
        raise TypeError("delete_archived_data() %s", ", ".join(messages))

    if not settings.ENABLE_S3_ARCHIVING:
        LOG.info("Skipping delete_archived_data. Upload feature is disabled.")
        return
    else:
        message = f"Deleting S3 data for {provider_type} provider {provider_uuid} in account {schema_name}."
        LOG.info(message)

    # We need to normalize capitalization and "-local" dev providers.
    account = schema_name[4:]

    path_prefix = f"{Config.WAREHOUSE_PATH}/{Config.CSV_DATA_TYPE}"
    prefix = f"{path_prefix}/{account}/{provider_uuid}/"
    LOG.info("Attempting to delete our archived data in S3 under %s", prefix)
    deleted_archived_with_prefix(settings.S3_BUCKET_NAME, prefix)

    path_prefix = f"{Config.WAREHOUSE_PATH}/{Config.PARQUET_DATA_TYPE}"
    prefix = f"{path_prefix}/{account}/{provider_uuid}/"
    LOG.info("Attempting to delete our archived data in S3 under %s", prefix)
    deleted_archived_with_prefix(settings.S3_BUCKET_NAME, prefix)


@app.task(
    name="masu.celery.tasks.sync_data_to_customer",
    queue_name="customer_data_sync",
    retry_kwargs={"max_retries": 5, "countdown": settings.COLD_STORAGE_RETRIVAL_WAIT_TIME},
)
def sync_data_to_customer(dump_request_uuid):
    """
    Scheduled task to sync normalized data to our customers S3 bucket.

    If the sync request raises SyncedFileInColdStorageError, this task
    will automatically retry in a set amount of time. This time is to give
    the storage solution time to retrieve a file from cold storage.
    This task will retry 5 times, and then fail.

    """
    dump_request = DataExportRequest.objects.get(uuid=dump_request_uuid)
    dump_request.status = DataExportRequest.PROCESSING
    dump_request.save()

    try:
        syncer = AwsS3Syncer(settings.S3_BUCKET_NAME)
        syncer.sync_bucket(
            dump_request.created_by.customer.schema_name,
            dump_request.bucket_name,
            (dump_request.start_date, dump_request.end_date),
        )
    except ClientError:
        LOG.exception(
            f"Encountered an error while processing DataExportRequest "
            f"{dump_request.uuid}, for {dump_request.created_by}."
        )
        dump_request.status = DataExportRequest.ERROR
        dump_request.save()
        return
    except SyncedFileInColdStorageError:
        LOG.info(
            f"One of the requested files is currently in cold storage for "
            f"DataExportRequest {dump_request.uuid}. This task will automatically retry."
        )
        dump_request.status = DataExportRequest.WAITING
        dump_request.save()
        try:
            raise sync_data_to_customer.retry(countdown=10, max_retries=5)
        except MaxRetriesExceededError:
            LOG.exception(
                f"Max retires exceeded for restoring a file in cold storage for "
                f"DataExportRequest {dump_request.uuid}, for {dump_request.created_by}."
            )
            dump_request.status = DataExportRequest.ERROR
            dump_request.save()
            return
    dump_request.status = DataExportRequest.COMPLETE
    dump_request.save()


@app.task(name="masu.celery.tasks.vacuum_schemas", queue_name="reporting")
def vacuum_schemas():
    """Vacuum all schemas."""
    tenants = Tenant.objects.values("schema_name")
    schema_names = [
        tenant.get("schema_name")
        for tenant in tenants
        if (tenant.get("schema_name") and tenant.get("schema_name") != "public")
    ]

    for schema_name in schema_names:
        LOG.info("Scheduling VACUUM task for %s", schema_name)
        vacuum_schema.delay(schema_name)


# This task will process the autovacuum tuning as a background process
@app.task(name="masu.celery.tasks.autovacuum_tune_schemas", queue_name="reporting")
def autovacuum_tune_schemas():
    """Set the autovacuum table settings based on table size for all schemata."""
    tenants = Tenant.objects.values("schema_name")
    schema_names = [
        tenant.get("schema_name")
        for tenant in tenants
        if (tenant.get("schema_name") and tenant.get("schema_name") != "public")
    ]

    for schema_name in schema_names:
        LOG.info("Scheduling autovacuum tune task for %s", schema_name)
        autovacuum_tune_schema.delay(schema_name)


@app.task(name="masu.celery.tasks.clean_volume", queue_name="clean_volume")
def clean_volume():
    """Clean up the volume in the worker pod."""
    LOG.info("Cleaning up the volume at %s " % Config.PVC_DIR)
    # get the billing months to use below
    months = DateAccessor().get_billing_months(Config.INITIAL_INGEST_NUM_MONTHS)
    db_accessor = ReportManifestDBAccessor()
    # this list is initialized with the .gitkeep file so that it does not get deleted
    assembly_ids_to_exclude = [".gitkeep"]
    # grab the assembly ids to exclude for each month
    for month in months:
        assembly_ids = db_accessor.get_last_seen_manifest_ids(month)
        assembly_ids_to_exclude.extend(assembly_ids)
    # now we want to loop through the files and clean up the ones that are not in the exclude list
    deleted_files = []
    retain_files = []

    datehelper = DateHelper()
    now = datehelper.now
    expiration_date = now - timedelta(seconds=Config.VOLUME_FILE_RETENTION)
    for [root, _, filenames] in os.walk(Config.PVC_DIR):
        for file in filenames:
            match = False
            for assembly_id in assembly_ids_to_exclude:
                if assembly_id in file:
                    match = True
            # if none of the assembly_ids that we care about were in the filename - we can safely delete it
            if not match:
                potential_delete = os.path.join(root, file)
                if os.path.exists(potential_delete):
                    file_datetime = datetime.fromtimestamp(os.path.getmtime(potential_delete))
                    file_datetime = timezone.make_aware(file_datetime)
                    if file_datetime < expiration_date:
                        os.remove(potential_delete)
                        deleted_files.append(potential_delete)
                    else:
                        retain_files.append(potential_delete)

    LOG.info("Removing all files older than %s", expiration_date)
    LOG.info("The following files were too new to delete: %s", retain_files)
    LOG.info("The following files were deleted: %s", deleted_files)


@app.task(name="masu.celery.tasks.crawl_account_hierarchy", queue_name="crawl_account_hierarchy")
def crawl_account_hierarchy(provider_uuid=None):
    """Crawl top level accounts to discover hierarchy."""
    if provider_uuid:
        _, polling_accounts = Orchestrator.get_accounts(provider_uuid=provider_uuid)
    else:
        _, polling_accounts = Orchestrator.get_accounts()
    LOG.info("Account hierarchy crawler found %s accounts to scan" % len(polling_accounts))
    processed = 0
    skipped = 0
    for account in polling_accounts:
        crawler = None

        # Look for a known crawler class to handle this provider
        if account.get("provider_type") == Provider.PROVIDER_AWS:
            crawler = AWSOrgUnitCrawler(account)

        if crawler:
            LOG.info(
                "Starting account hierarchy crawler for type {} with provider_uuid: {}".format(
                    account.get("provider_type"), account.get("provider_uuid")
                )
            )
            crawler.crawl_account_hierarchy()
            processed += 1
        else:
            LOG.info(
                "No known crawler for account with provider_uuid: {} of type {}".format(
                    account.get("provider_uuid"), account.get("provider_type")
                )
            )
            skipped += 1
    LOG.info(f"Account hierarchy crawler finished. {processed} processed and {skipped} skipped")
