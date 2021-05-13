# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounts(models.Model):
    account_id = models.CharField(primary_key=True, max_length=20)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    account_email = models.CharField(max_length=200, blank=True, null=True)
    account_desc = models.CharField(max_length=200, blank=True, null=True)
    account_addr = models.CharField(max_length=500, blank=True, null=True)
    account_type = models.CharField(max_length=20, blank=True, null=True)
    account_created_at = models.DateTimeField(blank=True, null=True)
    account_updated_at = models.DateTimeField(blank=True, null=True)
    account_archived = models.BooleanField(blank=True, null=True)
    account_archived_at = models.DateTimeField(blank=True, null=True)
    plan_id = models.IntegerField(blank=True, null=True)
    plan_name = models.CharField(max_length=20, blank=True, null=True)
    user_email = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'


class LoginCustomer(models.Model):
    # Field name made lowercase.
    customer_name = models.CharField(db_column='Customer_Name', max_length=50)
    # Field name made lowercase.
    customer_id = models.CharField(
        db_column='Customer_ID', primary_key=True, max_length=100)
    # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=50)
    # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30)
    # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=30)
    # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30)
    # Field name made lowercase.
    pincode = models.BigIntegerField(db_column='Pincode')
    # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200)
    # Field name made lowercase.
    user = models.OneToOneField(
        'LoginUser', models.DO_NOTHING, db_column='User_id')
    # Field name made lowercase.
    customer_photo = models.CharField(
        db_column='Customer_Photo', max_length=100)

    class Meta:
        managed = False
        db_table = 'login_customer'


class LoginManager(models.Model):
    # Field name made lowercase.
    manager_name = models.CharField(db_column='Manager_Name', max_length=50)
    # Field name made lowercase.
    manager_email_id = models.CharField(
        db_column='Manager_Email_ID', primary_key=True, max_length=50)
    # Field name made lowercase.
    mobile_no = models.CharField(db_column='Mobile_No', max_length=50)
    # Field name made lowercase.
    contact_no = models.CharField(db_column='Contact_No', max_length=50)
    # Field name made lowercase.
    customer_name = models.ForeignKey(
        LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')
    # Field name made lowercase.
    user = models.OneToOneField(
        'LoginUser', models.DO_NOTHING, db_column='User_id')

    class Meta:
        managed = False
        db_table = 'login_manager'


class LoginUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    is_customer = models.BooleanField()
    is_manager = models.BooleanField()
    is_user = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'login_user'


class LoginUserDetail(models.Model):
    # Field name made lowercase.
    user_name = models.CharField(db_column='User_Name', max_length=50)
    # Field name made lowercase.
    contact_person = models.CharField(
        db_column='Contact_Person', max_length=50)
    # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=50)
    # Field name made lowercase.
    contact1 = models.CharField(db_column='Contact1', max_length=50)
    # Field name made lowercase.
    contact2 = models.CharField(db_column='Contact2', max_length=50)
    # Field name made lowercase.
    device_id = models.CharField(
        db_column='Device_ID', primary_key=True, max_length=50)
    # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=50)
    # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)
    # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=30)
    # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30)
    # Field name made lowercase.
    pincode = models.BigIntegerField(db_column='Pincode')
    # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200)
    # Field name made lowercase.
    customer_name = models.ForeignKey(
        LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')
    # Field name made lowercase.
    manager_name = models.ForeignKey(
        LoginManager, models.DO_NOTHING, db_column='Manager_Name_id')
    # Field name made lowercase.
    user = models.OneToOneField(
        LoginUser, models.DO_NOTHING, db_column='User_id')

    class Meta:
        managed = False
        db_table = 'login_user_detail'


class Device(models.Model):
    device_id = models.CharField(primary_key=True, max_length=20)
    device_name = models.CharField(max_length=200, blank=True, null=True)
    device_desc = models.CharField(max_length=200, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True)
    account_id = models.CharField(max_length=20, blank=True, null=True)
    device_rating = models.FloatField(blank=True, null=True)
    device_location = models.CharField(max_length=200, blank=True, null=True)
    device_status = models.CharField(max_length=50, blank=True, null=True)
    device_created_at = models.DateTimeField(blank=True, null=True)
    device_updated_at = models.DateTimeField(blank=True, null=True)
    fuel_report_link = models.CharField(max_length=200, blank=True, null=True)
    operational_report_link = models.CharField(
        max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceOperational(models.Model):
    device_id = models.CharField(max_length=20, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    fuel_level = models.FloatField(blank=True, null=True)
    unit_generated_kwh = models.FloatField(blank=True, null=True)
    fuel_consumed = models.FloatField(blank=True, null=True)
    energy_generated_kwh = models.FloatField(blank=True, null=True)
    carbon_footprint = models.FloatField(blank=True, null=True)
    fuel_cost = models.FloatField(blank=True, null=True)
    per_unit_cost = models.FloatField(blank=True, null=True)
    run_hours = models.FloatField(blank=True, null=True)
    maximum_demand_load = models.FloatField(blank=True, null=True)
    efficiency = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_operational'


class DevicesInfo(models.Model):
    device_header = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    device_time = models.DateTimeField()
    gateway_device_battery = models.FloatField(blank=True, null=True)
    room_temperature = models.FloatField(blank=True, null=True)
    dg_battery_voltage = models.FloatField(blank=True, null=True)
    gateway_power_status = models.IntegerField(blank=True, null=True)
    gsm_signal = models.IntegerField(blank=True, null=True)
    energy_output_kw_total = models.FloatField(blank=True, null=True)
    kva_r_phase = models.FloatField(blank=True, null=True)
    kva_y_phase = models.FloatField(blank=True, null=True)
    kva_b_phase = models.FloatField(blank=True, null=True)
    power_factor = models.FloatField(blank=True, null=True)
    energy_output_kva = models.FloatField(blank=True, null=True)
    vll_average = models.FloatField(blank=True, null=True)
    vry_phase_voltage = models.FloatField(blank=True, null=True)
    vyb_phase_voltage = models.FloatField(blank=True, null=True)
    vbr_phase_voltage = models.FloatField(blank=True, null=True)
    vln_average = models.FloatField(blank=True, null=True)
    vr_phase_voltage = models.FloatField(blank=True, null=True)
    vy_phase_voltage = models.FloatField(blank=True, null=True)
    vb_phase_voltage = models.FloatField(blank=True, null=True)
    current_average = models.FloatField(blank=True, null=True)
    current_r_phase = models.FloatField(blank=True, null=True)
    current_y_phase = models.FloatField(blank=True, null=True)
    current_b_phase = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    unit_generated_kwh = models.FloatField(blank=True, null=True)
    rpm = models.FloatField(blank=True, null=True)
    dg_runtime_seconds = models.IntegerField(blank=True, null=True)
    fuel_level_percentage = models.IntegerField(blank=True, null=True)
    fuel_level_litre = models.IntegerField(blank=True, null=True)
    fuel_level_volt = models.IntegerField(blank=True, null=True)
    fuel_level_mm = models.IntegerField(blank=True, null=True)
    rpm_ctrl = models.IntegerField(blank=True, null=True)
    dg_counter_ctrl = models.IntegerField(blank=True, null=True)
    runtime_second_ctrl = models.IntegerField(blank=True, null=True)
    device_status = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devices_info'
