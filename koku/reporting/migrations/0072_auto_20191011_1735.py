# Generated by Django 2.2.4 on 2019-10-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0071_auto_20190926_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awscostentryproduct',
            name='product_name',
            field=models.TextField(null=True),
        ),
    ]