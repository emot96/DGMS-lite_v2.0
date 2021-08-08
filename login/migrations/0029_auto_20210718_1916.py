# Generated by Django 3.1.7 on 2021-07-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0028_auto_20210703_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThresholdDetails',
            fields=[
                ('alert_type_id', models.IntegerField(blank=True, null=True)),
                ('alert_type_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('device_rating', models.FloatField()),
                ('threshold_name', models.CharField(blank=True, max_length=50, null=True)),
                ('threshold_type', models.CharField(blank=True, max_length=1, null=True)),
                ('threshold_value', models.FloatField(blank=True, null=True)),
                ('operator', models.CharField(blank=True, max_length=1, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'threshold_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ThresholdMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('threshold_operator', models.CharField(max_length=1)),
                ('energy_output_kva', models.FloatField(blank=True, null=True)),
                ('energy_output_kw_total', models.FloatField(blank=True, null=True)),
                ('current_r_phase', models.FloatField(blank=True, null=True)),
                ('current_y_phase', models.FloatField(blank=True, null=True)),
                ('current_b_phase', models.FloatField(blank=True, null=True)),
                ('vll_average', models.FloatField(blank=True, null=True)),
                ('frequency', models.FloatField(blank=True, null=True)),
                ('power_factor', models.FloatField(blank=True, null=True)),
                ('rpm', models.FloatField(blank=True, null=True)),
                ('rpm_ctrl', models.FloatField(blank=True, null=True)),
                ('fuel_level_percentage', models.FloatField(blank=True, null=True)),
                ('dg_battery_voltage', models.FloatField(blank=True, null=True)),
                ('gateway_device_battery', models.FloatField(blank=True, null=True)),
                ('gsm_signal', models.FloatField(blank=True, null=True)),
                ('room_temperature', models.FloatField(blank=True, null=True)),
                ('device_phase', models.IntegerField()),
            ],
            options={
                'db_table': 'threshold_metadata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ThresholdMetadataOld',
            fields=[
                ('rating', models.FloatField(primary_key=True, serialize=False)),
                ('threshold_operator', models.CharField(max_length=1)),
                ('energy_output_kva', models.FloatField(blank=True, null=True)),
                ('energy_output_kw_total', models.FloatField(blank=True, null=True)),
                ('current_r_phase', models.FloatField(blank=True, null=True)),
                ('current_y_phase', models.FloatField(blank=True, null=True)),
                ('current_b_phase', models.FloatField(blank=True, null=True)),
                ('vll_average', models.FloatField(blank=True, null=True)),
                ('frequency', models.FloatField(blank=True, null=True)),
                ('power_factor', models.FloatField(blank=True, null=True)),
                ('rpm', models.FloatField(blank=True, null=True)),
                ('rpm_ctrl', models.FloatField(blank=True, null=True)),
                ('fuel_level_percentage', models.FloatField(blank=True, null=True)),
                ('dg_battery_voltage', models.FloatField(blank=True, null=True)),
                ('gateway_device_battery', models.FloatField(blank=True, null=True)),
                ('gsm_signal', models.FloatField(blank=True, null=True)),
                ('room_temperature', models.FloatField(blank=True, null=True)),
                ('device_phase', models.IntegerField()),
            ],
            options={
                'db_table': 'threshold_metadata_old',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='service_history',
            name='Service_Document',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
