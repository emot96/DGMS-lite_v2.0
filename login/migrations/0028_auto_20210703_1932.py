# Generated by Django 3.1.7 on 2021-07-03 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0027_auto_20210701_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_history',
            name='Battery_Last_Replacement_Date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='service_history',
            name='Battery_Next_Replacement_Date',
            field=models.DateField(blank=True),
        ),
    ]