# Generated by Django 3.1.7 on 2021-06-05 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0017_auto_20210605_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ups_asset',
            name='Battery_Replacement_Date',
        ),
    ]
