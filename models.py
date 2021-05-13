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


class AlertType(models.Model):
    alert_type_id = models.AutoField(primary_key=True)
    alert_type_name = models.CharField(max_length=50, blank=True, null=True)
    alert_type_desc = models.CharField(max_length=100, blank=True, null=True)
    alert_cat = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alert_type'


class Alerts(models.Model):
    alert_id = models.AutoField(primary_key=True)
    alert_type_name = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    alert_open = models.BooleanField(blank=True, null=True)
    alert_level = models.CharField(max_length=1, blank=True, null=True)
    param_value = models.FloatField(blank=True, null=True)
    param_threshold_value = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alerts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BackupDeviceOperational(models.Model):
    id = models.IntegerField(blank=True, null=True)
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
        db_table = 'backup_device_operational'


class BackupDevicesInfo(models.Model):
    id = models.IntegerField(blank=True, null=True)
    device_header = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    device_time = models.DateTimeField(blank=True, null=True)
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
        db_table = 'backup_devices_info'


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
    operational_report_link = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DeviceCounter(models.Model):
    device_id = models.CharField(max_length=20, blank=True, null=True)
    counter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_counter'


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


class DeviceRunningWithoutLoad(models.Model):
    id = models.AutoField()
    device_id = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    device_rwl_for = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_running_without_load'


class DevicesInfo(models.Model):
    id = models.AutoField()
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


class DevicesInfoOld(models.Model):
    id = models.AutoField()
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
        db_table = 'devices_info_old'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('LoginUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FuelMmCapacityInLitre(models.Model):
    device_id = models.CharField(max_length=50, blank=True, null=True)
    fuel_capacity_per_mm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fuel_mm_capacity_in_litre'


class LoginAsset(models.Model):
    device_id = models.OneToOneField('LoginUserDetail', models.DO_NOTHING, db_column='Device_ID_id', primary_key=True)  # Field name made lowercase.
    asset_name = models.CharField(db_column='Asset_Name', max_length=50)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=50)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200)  # Field name made lowercase.
    asset_photo = models.CharField(db_column='Asset_Photo', max_length=100)  # Field name made lowercase.
    diesel_tank_size = models.BigIntegerField(db_column='Diesel_Tank_Size')  # Field name made lowercase.
    rating_in_kva = models.CharField(db_column='Rating_In_KVA', max_length=50)  # Field name made lowercase.
    oem = models.CharField(db_column='OEM', max_length=50)  # Field name made lowercase.
    seller_name = models.CharField(db_column='Seller_Name', max_length=50)  # Field name made lowercase.
    warranty_start_date = models.DateField(db_column='Warranty_Start_Date')  # Field name made lowercase.
    warranty_end_date = models.DateField(db_column='Warranty_End_Date')  # Field name made lowercase.
    warranty_period = models.CharField(db_column='Warranty_Period', max_length=50)  # Field name made lowercase.
    warranty_status = models.CharField(db_column='Warranty_Status', max_length=20)  # Field name made lowercase.
    date_of_installation = models.DateField(db_column='Date_Of_Installation')  # Field name made lowercase.
    commissioning_date = models.DateField(db_column='Commissioning_Date')  # Field name made lowercase.
    operations = models.CharField(db_column='Operations', max_length=20)  # Field name made lowercase.
    engine_make = models.CharField(db_column='Engine_Make', max_length=50)  # Field name made lowercase.
    engine_model_no = models.CharField(db_column='Engine_Model_No', max_length=50)  # Field name made lowercase.
    engine_s_no = models.CharField(db_column='Engine_S_NO', max_length=50)  # Field name made lowercase.
    engine_other_info = models.CharField(db_column='Engine_Other_Info', max_length=500)  # Field name made lowercase.
    alternator_make = models.CharField(db_column='Alternator_Make', max_length=50)  # Field name made lowercase.
    alternator_model_no = models.CharField(db_column='Alternator_Model_No', max_length=50)  # Field name made lowercase.
    alternator_s_no = models.CharField(db_column='Alternator_S_NO', max_length=50)  # Field name made lowercase.
    alternator_other_info = models.CharField(db_column='Alternator_Other_Info', max_length=500)  # Field name made lowercase.
    battery_make = models.CharField(db_column='Battery_Make', max_length=50)  # Field name made lowercase.
    battery_model_no = models.CharField(db_column='Battery_Model_No', max_length=50)  # Field name made lowercase.
    battery_s_no = models.CharField(db_column='Battery_S_NO', max_length=50)  # Field name made lowercase.
    battery_other_info = models.CharField(db_column='Battery_Other_Info', max_length=500)  # Field name made lowercase.
    battery_charger_make = models.CharField(db_column='Battery_Charger_Make', max_length=50)  # Field name made lowercase.
    battery_charger_model_no = models.CharField(db_column='Battery_Charger_Model_No', max_length=50)  # Field name made lowercase.
    battery_charger_s_no = models.CharField(db_column='Battery_Charger_S_NO', max_length=50)  # Field name made lowercase.
    battery_charger_other_info = models.CharField(db_column='Battery_Charger_Other_Info', max_length=500)  # Field name made lowercase.
    customer_name = models.ForeignKey('LoginCustomer', models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_asset'


class LoginBeforeDgmaInstallation(models.Model):
    device_id = models.OneToOneField('LoginUserDetail', models.DO_NOTHING, db_column='Device_ID_id', primary_key=True)  # Field name made lowercase.
    previous_run_hour = models.CharField(db_column='Previous_Run_Hour', max_length=50)  # Field name made lowercase.
    previous_fuel_consumed = models.CharField(db_column='Previous_Fuel_Consumed', max_length=50)  # Field name made lowercase.
    run_count = models.CharField(db_column='Run_Count', max_length=50)  # Field name made lowercase.
    units_generated = models.CharField(db_column='Units_Generated', max_length=50)  # Field name made lowercase.
    customer_name = models.ForeignKey('LoginCustomer', models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_before_dgma_installation'


class LoginCustomer(models.Model):
    customer_name = models.CharField(db_column='Customer_Name', max_length=50)  # Field name made lowercase.
    customer_id = models.CharField(db_column='Customer_ID', primary_key=True, max_length=100)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=30)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=30)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30)  # Field name made lowercase.
    pincode = models.BigIntegerField(db_column='Pincode')  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200)  # Field name made lowercase.
    user = models.OneToOneField('LoginUser', models.DO_NOTHING, db_column='User_id')  # Field name made lowercase.
    customer_photo = models.CharField(db_column='Customer_Photo', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_customer'


class LoginDgmsDeviceInfo(models.Model):
    device_id = models.OneToOneField('LoginUserDetail', models.DO_NOTHING, db_column='Device_ID_id', primary_key=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=50)  # Field name made lowercase.
    device_serial_no = models.CharField(db_column='Device_Serial_No', max_length=50)  # Field name made lowercase.
    sim_card = models.CharField(db_column='Sim_Card', max_length=50)  # Field name made lowercase.
    imei_no = models.CharField(db_column='IMEI_No', max_length=100)  # Field name made lowercase.
    other = models.CharField(db_column='Other', max_length=200)  # Field name made lowercase.
    other_info = models.CharField(db_column='Other_Info', max_length=500)  # Field name made lowercase.
    customer_name = models.ForeignKey(LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.
    dgms_date_of_installation = models.DateField(db_column='DGMS_Date_Of_Installation')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_dgms_device_info'


class LoginManager(models.Model):
    manager_name = models.CharField(db_column='Manager_Name', max_length=50)  # Field name made lowercase.
    manager_email_id = models.CharField(db_column='Manager_Email_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    mobile_no = models.CharField(db_column='Mobile_No', max_length=50)  # Field name made lowercase.
    contact_no = models.CharField(db_column='Contact_No', max_length=50)  # Field name made lowercase.
    customer_name = models.ForeignKey(LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.
    user = models.OneToOneField('LoginUser', models.DO_NOTHING, db_column='User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_manager'


class LoginPrice(models.Model):
    location = models.CharField(db_column='Location', primary_key=True, max_length=50)  # Field name made lowercase.
    energy_price = models.CharField(db_column='Energy_Price', max_length=50)  # Field name made lowercase.
    diesel_price = models.CharField(db_column='Diesel_Price', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_price'


class LoginSensorInfo(models.Model):
    device_id = models.OneToOneField('LoginUserDetail', models.DO_NOTHING, db_column='Device_ID_id', primary_key=True)  # Field name made lowercase.
    energy_meter_make_info = models.CharField(db_column='Energy_Meter_Make_Info', max_length=50)  # Field name made lowercase.
    energy_meter_model_no = models.CharField(db_column='Energy_Meter_Model_No', max_length=50)  # Field name made lowercase.
    energy_meter_s_no = models.CharField(db_column='Energy_Meter_S_No', max_length=50)  # Field name made lowercase.
    current_transformer_make_info = models.CharField(db_column='Current_Transformer_Make_Info', max_length=50)  # Field name made lowercase.
    current_transformer_model_no = models.CharField(db_column='Current_Transformer_Model_No', max_length=50)  # Field name made lowercase.
    current_transformer_s_no = models.CharField(db_column='Current_Transformer_S_No', max_length=50)  # Field name made lowercase.
    current_transformer_ct_ratio = models.CharField(db_column='Current_Transformer_CT_Ratio', max_length=50)  # Field name made lowercase.
    fuel_sensor_make_info = models.CharField(db_column='Fuel_Sensor_Make_Info', max_length=50)  # Field name made lowercase.
    fuel_sensor_model_no = models.CharField(db_column='Fuel_Sensor_Model_No', max_length=50)  # Field name made lowercase.
    fuel_sensors_no = models.CharField(db_column='Fuel_SensorS_No', max_length=50)  # Field name made lowercase.
    fuel_sensor_length = models.CharField(db_column='Fuel_Sensor_Length', max_length=50)  # Field name made lowercase.
    customer_name = models.ForeignKey(LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_sensor_info'


class LoginServiceHistory(models.Model):
    device_id = models.OneToOneField('LoginUserDetail', models.DO_NOTHING, db_column='Device_ID_id', primary_key=True)  # Field name made lowercase.
    service_contract = models.CharField(db_column='Service_Contract', max_length=20)  # Field name made lowercase.
    service_provider = models.CharField(db_column='Service_Provider', max_length=100)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100)  # Field name made lowercase.
    contact = models.CharField(db_column='Contact', max_length=20)  # Field name made lowercase.
    last_service_date = models.DateField(db_column='Last_Service_Date')  # Field name made lowercase.
    activity = models.CharField(db_column='Activity', max_length=300)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=300)  # Field name made lowercase.
    next_service_date = models.DateField(db_column='Next_Service_Date')  # Field name made lowercase.
    customer_name = models.ForeignKey(LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.
    activity1 = models.CharField(db_column='Activity1', max_length=300)  # Field name made lowercase.
    remark1 = models.CharField(db_column='Remark1', max_length=300)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_service_history'


class LoginSetalert(models.Model):
    kva_rating = models.BigIntegerField(db_column='KVA_Rating')  # Field name made lowercase.
    alert = models.CharField(db_column='Alert', max_length=50)  # Field name made lowercase.
    less_than = models.CharField(db_column='Less_Than', max_length=30)  # Field name made lowercase.
    more_than = models.CharField(db_column='More_Than', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_setalert'


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
    user_name = models.CharField(db_column='User_Name', max_length=50)  # Field name made lowercase.
    contact_person = models.CharField(db_column='Contact_Person', max_length=50)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_ID', max_length=50)  # Field name made lowercase.
    contact1 = models.CharField(db_column='Contact1', max_length=50)  # Field name made lowercase.
    contact2 = models.CharField(db_column='Contact2', max_length=50)  # Field name made lowercase.
    device_id = models.CharField(db_column='Device_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=50)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=30)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30)  # Field name made lowercase.
    pincode = models.BigIntegerField(db_column='Pincode')  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200)  # Field name made lowercase.
    customer_name = models.ForeignKey(LoginCustomer, models.DO_NOTHING, db_column='Customer_Name_id')  # Field name made lowercase.
    manager_name = models.ForeignKey(LoginManager, models.DO_NOTHING, db_column='Manager_Name_id')  # Field name made lowercase.
    user = models.OneToOneField(LoginUser, models.DO_NOTHING, db_column='User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_user_detail'


class LoginUserGroups(models.Model):
    user = models.ForeignKey(LoginUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_user_groups'
        unique_together = (('user', 'group'),)


class LoginUserUserPermissions(models.Model):
    user = models.ForeignKey(LoginUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_user_user_permissions'
        unique_together = (('user', 'permission'),)


class NotificationSettings(models.Model):
    notification_setting_id = models.AutoField(primary_key=True)
    account_id = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification_settings'


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    notification_type = models.CharField(max_length=50, blank=True, null=True)
    notification_setting_id = models.IntegerField(blank=True, null=True)
    notification_status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class OpenAlerts(models.Model):
    device_id = models.CharField(max_length=50, blank=True, null=True)
    alert_type_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'open_alerts'


class TempBackupDevicesInfo(models.Model):
    id = models.IntegerField(blank=True, null=True)
    device_header = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    device_time = models.DateTimeField(blank=True, null=True)
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
        db_table = 'temp_backup_devices_info'


class ThresholdDetails(models.Model):
    threshold_id = models.AutoField()
    alert_type_id = models.IntegerField(blank=True, null=True)
    alert_type_name = models.CharField(primary_key=True, max_length=50)
    device_rating = models.FloatField()
    threshold_name = models.CharField(max_length=50, blank=True, null=True)
    threshold_type = models.CharField(max_length=1, blank=True, null=True)
    threshold_value = models.FloatField(blank=True, null=True)
    operator = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'threshold_details'
        unique_together = (('alert_type_name', 'device_rating'),)


class ThresholdMetadata(models.Model):
    rating = models.FloatField(primary_key=True)
    threshold_operator = models.CharField(max_length=1)
    energy_output_kva = models.FloatField(blank=True, null=True)
    energy_output_kw_total = models.FloatField(blank=True, null=True)
    current_r_phase = models.FloatField(blank=True, null=True)
    current_y_phase = models.FloatField(blank=True, null=True)
    current_b_phase = models.FloatField(blank=True, null=True)
    vll_average = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    power_factor = models.FloatField(blank=True, null=True)
    rpm = models.FloatField(blank=True, null=True)
    rpm_ctrl = models.FloatField(blank=True, null=True)
    fuel_level_percentage = models.FloatField(blank=True, null=True)
    dg_battery_voltage = models.FloatField(blank=True, null=True)
    gateway_device_battery = models.FloatField(blank=True, null=True)
    gsm_signal = models.FloatField(blank=True, null=True)
    room_temperature = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'threshold_metadata'
        unique_together = (('rating', 'threshold_operator'),)
