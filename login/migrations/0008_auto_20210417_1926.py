# Generated by Django 3.1.7 on 2021-04-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alerts_alerttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_history',
            name='Activity1',
            field=models.CharField(default='NULL', max_length=300),
        ),
        migrations.AddField(
            model_name='service_history',
            name='Remark1',
            field=models.CharField(default='NULL', max_length=300),
        ),
    ]