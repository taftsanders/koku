# Generated by Django 2.2.4 on 2019-11-01 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_auto_20191022_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]