# Generated by Django 3.1.7 on 2021-06-12 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_auto_20210612_1303'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ups_asset',
            old_name='Date_Of_Installation',
            new_name='UPS_EMS_Date_Of_Installation',
        ),
    ]