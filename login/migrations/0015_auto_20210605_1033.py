# Generated by Django 3.1.7 on 2021-06-05 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_auto_20210604_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ups_service_history',
            old_name='Battery_Last_Service_Date',
            new_name='Battery_Last_Replaced_Date',
        ),
        migrations.RenameField(
            model_name='ups_service_history',
            old_name='Battery_Next_Service_Date',
            new_name='Battery_Next_Replacment_Date',
        ),
        migrations.RemoveField(
            model_name='ups_asset',
            name='Voltage_Range',
        ),
        migrations.AddField(
            model_name='ups_asset',
            name='Battery_Date_Of_Installation',
            field=models.DateField(default=datetime.datetime(2021, 6, 5, 10, 33, 26, 667941), max_length=50),
        ),
        migrations.AddField(
            model_name='ups_asset',
            name='UPS_Type',
            field=models.CharField(default='SP IN-SP OUT', max_length=70),
        ),
    ]
