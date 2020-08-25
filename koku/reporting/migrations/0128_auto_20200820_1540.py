# Generated by Django 2.2.15 on 2020-08-20 15:40
import pkgutil

from django.db import connection
from django.db import migrations


def add_views(apps, schema_editor):
    """Create database VIEWS from files."""
    view_sql = pkgutil.get_data("reporting.provider.ocp", f"sql/views/reporting_ocp_pod_summary_by_project.sql")
    view_sql = view_sql.decode("utf-8")
    with connection.cursor() as cursor:
        cursor.execute(view_sql)

    view_sql = pkgutil.get_data("reporting.provider.ocp", f"sql/views/reporting_ocp_pod_summary.sql")
    view_sql = view_sql.decode("utf-8")
    with connection.cursor() as cursor:
        cursor.execute(view_sql)


class Migration(migrations.Migration):

    dependencies = [("reporting", "0127_ocpazure_unit_normalization")]

    operations = [
        migrations.RemoveField(model_name="ocpusagelineitemdaily", name="total_capacity_cpu_core_seconds"),
        migrations.RemoveField(model_name="ocpusagelineitemdaily", name="total_capacity_memory_byte_seconds"),
        migrations.RemoveField(model_name="ocpusagelineitemdailysummary", name="total_capacity_cpu_core_hours"),
        migrations.RemoveField(model_name="ocpusagelineitemdailysummary", name="total_capacity_memory_gigabyte_hours"),
        migrations.RunPython(add_views),
    ]
