# Generated by Django 3.1.7 on 2021-04-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_dgms_device_info_dgms_date_of_installation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerts',
            fields=[
                ('alert_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_type_name', models.CharField(blank=True, max_length=50, null=True)),
                ('device_id', models.CharField(blank=True, max_length=50, null=True)),
                ('alert_open', models.BooleanField(blank=True, null=True)),
                ('alert_level', models.CharField(blank=True, max_length=1, null=True)),
                ('param_value', models.FloatField(blank=True, null=True)),
                ('param_threshold_value', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'alerts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AlertType',
            fields=[
                ('alert_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('alert_type_name', models.CharField(blank=True, max_length=50, null=True)),
                ('alert_type_desc', models.CharField(blank=True, max_length=100, null=True)),
                ('alert_cat', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'alert_type',
                'managed': False,
            },
        ),
    ]