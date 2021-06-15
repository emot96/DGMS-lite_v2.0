# Generated by Django 3.1.7 on 2021-06-12 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0020_auto_20210606_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='ups_asset',
            name='Date_Of_Installation',
            field=models.DateField(default=datetime.datetime(2021, 6, 12, 13, 2, 49, 187799)),
        ),
        migrations.AlterField(
            model_name='ups_asset',
            name='Battery_Date_Of_Installation',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ups_asset',
            name='Battery_Warranty_End_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ups_asset',
            name='Battery_Warranty_Start_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ups_asset',
            name='UPS_Date_Of_Installation',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ups_asset',
            name='UPS_Warranty_End_Date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='ups_asset',
            name='UPS_Warranty_Start_Date',
            field=models.DateField(),
        ),
    ]
