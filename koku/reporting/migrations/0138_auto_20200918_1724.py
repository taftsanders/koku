# Generated by Django 2.2.15 on 2020-09-18 17:24
import uuid

import django.contrib.postgres.fields
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("reporting", "0137_partitioned_tables_triggers")]

    operations = [
        migrations.RunSQL(
            """
            TRUNCATE TABLE reporting_ocpstoragevolumelabel_summary CASCADE;
            TRUNCATE TABLE reporting_ocpusagepodlabel_summary CASCADE;
            TRUNCATE TABLE reporting_ocptags_values CASCADE;

            TRUNCATE TABLE reporting_awstags_summary CASCADE;
            TRUNCATE TABLE reporting_awstags_values CASCADE;

            TRUNCATE TABLE reporting_azuretags_summary CASCADE;
            TRUNCATE TABLE reporting_azuretags_values CASCADE;

            TRUNCATE TABLE reporting_ocpawstags_summary CASCADE;
            TRUNCATE TABLE reporting_ocpawstags_values CASCADE;

            TRUNCATE TABLE reporting_ocpazuretags_summary CASCADE;
            TRUNCATE TABLE reporting_ocpazuretags_values CASCADE;
            """
        ),
        migrations.RemoveField(model_name="awstagssummary", name="id"),
        migrations.RemoveField(model_name="awstagssummary", name="values_mtm"),
        migrations.RemoveField(model_name="azuretagssummary", name="id"),
        migrations.RemoveField(model_name="azuretagssummary", name="values_mtm"),
        migrations.RemoveField(model_name="ocpstoragevolumelabelsummary", name="id"),
        migrations.RemoveField(model_name="ocpstoragevolumelabelsummary", name="values_mtm"),
        migrations.RemoveField(model_name="ocpusagepodlabelsummary", name="id"),
        migrations.RemoveField(model_name="ocpusagepodlabelsummary", name="values_mtm"),
        migrations.RemoveField(model_name="awstagsvalues", name="id"),
        migrations.RemoveField(model_name="azuretagsvalues", name="id"),
        migrations.RemoveField(model_name="ocptagsvalues", name="id"),
        migrations.RemoveField(model_name="ocpazuretagsvalues", name="id"),
        migrations.RemoveField(model_name="ocpawstagssummary", name="id"),
        migrations.RemoveField(model_name="ocpawstagsvalues", name="id"),
        migrations.RemoveField(model_name="ocpazuretagssummary", name="id"),
        migrations.RemoveField(model_name="ocpawstagssummary", name="cluster_alias"),
        migrations.RemoveField(model_name="ocpawstagssummary", name="cluster_id"),
        migrations.RemoveField(model_name="ocpazuretagssummary", name="cluster_alias"),
        migrations.RemoveField(model_name="ocpazuretagssummary", name="cluster_id"),
        migrations.RemoveField(model_name="ocpazuretagssummary", name="values_mtm"),
        migrations.RemoveField(model_name="ocpawstagssummary", name="values_mtm"),
        migrations.AddField(
            model_name="awstagssummary",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="awstagsvalues", name="key", field=models.TextField(default=""), preserve_default=False
        ),
        migrations.AddField(
            model_name="awstagsvalues",
            name="usage_account_ids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="awstagsvalues",
            name="account_aliases",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="awstagsvalues",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="azuretagssummary",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="azuretagsvalues", name="key", field=models.TextField(default=""), preserve_default=False
        ),
        migrations.AddField(
            model_name="azuretagsvalues",
            name="subscription_guids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="azuretagsvalues",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(model_name="ocpstoragevolumelabelsummary", name="node", field=models.TextField(null=True)),
        migrations.AddField(
            model_name="ocpstoragevolumelabelsummary",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="ocptagsvalues", name="key", field=models.TextField(default=""), preserve_default=False
        ),
        migrations.AddField(
            model_name="ocptagsvalues",
            name="cluster_ids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocptagsvalues",
            name="cluster_aliases",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocptagsvalues",
            name="nodes",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name="ocptagsvalues",
            name="namespaces",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocptagsvalues",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(model_name="ocpusagepodlabelsummary", name="node", field=models.TextField(null=True)),
        migrations.AddField(
            model_name="ocpusagepodlabelsummary",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(model_name="awstagssummary", name="key", field=models.TextField()),
        migrations.AlterField(model_name="awstagssummary", name="usage_account_id", field=models.TextField(null=True)),
        migrations.AlterField(
            model_name="awstagssummary",
            name="values",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None),
        ),
        migrations.AlterField(model_name="awstagsvalues", name="value", field=models.TextField()),
        migrations.AlterField(model_name="azuretagssummary", name="key", field=models.TextField()),
        migrations.AlterField(
            model_name="azuretagssummary",
            name="values",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None),
        ),
        migrations.AlterField(model_name="azuretagsvalues", name="value", field=models.TextField()),
        migrations.AlterField(model_name="ocpstoragevolumelabelsummary", name="key", field=models.TextField()),
        migrations.AlterField(model_name="ocpstoragevolumelabelsummary", name="namespace", field=models.TextField()),
        migrations.AlterField(
            model_name="ocpstoragevolumelabelsummary",
            name="values",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None),
        ),
        migrations.AlterField(model_name="ocptagsvalues", name="value", field=models.TextField()),
        migrations.AlterField(model_name="ocpusagepodlabelsummary", name="key", field=models.TextField()),
        migrations.AlterField(model_name="ocpusagepodlabelsummary", name="namespace", field=models.TextField()),
        migrations.AlterField(
            model_name="ocpusagepodlabelsummary",
            name="values",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None),
        ),
        migrations.AlterUniqueTogether(name="awstagsvalues", unique_together={("key", "value")}),
        migrations.AlterUniqueTogether(name="azuretagsvalues", unique_together={("key", "value")}),
        migrations.AlterUniqueTogether(name="ocptagsvalues", unique_together={("key", "value")}),
        migrations.AddIndex(
            model_name="awstagsvalues", index=models.Index(fields=["key"], name="aws_tags_value_key_idx")
        ),
        migrations.AddIndex(
            model_name="azuretagsvalues", index=models.Index(fields=["key"], name="azure_tags_value_key_idx")
        ),
        migrations.AddIndex(
            model_name="ocptagsvalues", index=models.Index(fields=["key"], name="openshift_tags_value_key_idx")
        ),
        migrations.AddField(model_name="ocpawstagssummary", name="node", field=models.TextField(null=True)),
        migrations.AddField(
            model_name="ocpawstagssummary",
            name="report_period",
            field=models.ForeignKey(
                default="", on_delete=django.db.models.deletion.CASCADE, to="reporting.OCPUsageReportPeriod"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpawstagssummary",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues", name="key", field=models.TextField(default=""), preserve_default=False
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="account_aliases",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="cluster_aliases",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="cluster_ids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="namespaces",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="nodes",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="usage_account_ids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpawstagsvalues",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(model_name="ocpazuretagssummary", name="node", field=models.TextField(null=True)),
        migrations.AddField(
            model_name="ocpazuretagssummary",
            name="report_period",
            field=models.ForeignKey(
                default="", on_delete=django.db.models.deletion.CASCADE, to="reporting.OCPUsageReportPeriod"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpazuretagssummary",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues", name="key", field=models.TextField(default=""), preserve_default=False
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues",
            name="cluster_aliases",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues",
            name="cluster_ids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues",
            name="namespaces",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues",
            name="nodes",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues",
            name="subscription_guids",
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ocpazuretagsvalues",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="ocpawstagssummary",
            name="namespace",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(model_name="ocpawstagsvalues", name="value", field=models.TextField()),
        migrations.AlterField(
            model_name="ocpazuretagssummary",
            name="namespace",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AlterField(model_name="ocpazuretagsvalues", name="value", field=models.TextField()),
        migrations.AlterUniqueTogether(
            name="ocpawstagssummary",
            unique_together={("key", "cost_entry_bill", "report_period", "usage_account_id", "namespace")},
        ),
        migrations.AlterUniqueTogether(name="ocpawstagsvalues", unique_together={("key", "value")}),
        migrations.AlterUniqueTogether(
            name="ocpazuretagssummary",
            unique_together={("key", "cost_entry_bill", "report_period", "subscription_guid", "namespace")},
        ),
        migrations.AddIndex(
            model_name="ocpawstagsvalues", index=models.Index(fields=["key"], name="ocp_aws_tags_value_key_idx")
        ),
        migrations.AlterUniqueTogether(name="ocpazuretagsvalues", unique_together={("key", "value")}),
        migrations.AddIndex(
            model_name="ocpazuretagsvalues", index=models.Index(fields=["key"], name="ocp_azure_tags_value_key_idx")
        ),
    ]
