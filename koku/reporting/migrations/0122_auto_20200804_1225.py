# Generated by Django 2.2.12 on 2020-08-04 12:25
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting_common", "0024_remove_costusagereportmanifest_num_processed_files"),
        ("api", "0020_sources_out_of_order_delete"),
        ("reporting", "0121_auto_20200728_2258"),
    ]

    operations = [
        migrations.AddField(
            model_name="awscostentrybill",
            name="manifest",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting_common.CostUsageReportManifest"
            ),
        ),
        migrations.AddField(
            model_name="azurecostentrybill",
            name="manifest",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting_common.CostUsageReportManifest"
            ),
        ),
        migrations.AddField(
            model_name="ocpusagereportperiod",
            name="manifest",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting_common.CostUsageReportManifest"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="awscostentrybill",
            unique_together={("bill_type", "payer_account_id", "billing_period_start", "provider", "manifest")},
        ),
        migrations.AlterUniqueTogether(
            name="azurecostentrybill", unique_together={("billing_period_start", "provider", "manifest")}
        ),
        migrations.AlterUniqueTogether(
            name="ocpusagereportperiod",
            unique_together={("cluster_id", "report_period_start", "provider", "manifest")},
        ),
    ]
