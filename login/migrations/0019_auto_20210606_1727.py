# Generated by Django 3.1.7 on 2021-06-06 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_remove_ups_asset_battery_replacement_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ems_asset',
            name='Service_Provider',
        ),
        migrations.RemoveField(
            model_name='ups_asset',
            name='Service_Provider',
        ),
    ]