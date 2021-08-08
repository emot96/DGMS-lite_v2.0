import datetime
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.base import Model
from django.contrib.auth.models import AbstractUser, BaseUserManager, update_last_login
from django.db.models.fields import AutoField, CharField
from django.db.models.manager import Manager
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

# Create your models here.

STATUS = (
    ("YES", "YES"),
    ("NO", "NO"),
)

PHASE = (
    ("SINGLE PHASE", "SINGLE PHASE"),
    ("TRIPLE PHASE", "TRIPLE PHASE"),
)

COOLING = (
    ("AIR COOLED", "AIR COOLED"),
    ("OIL COOLED", "OIL COOLED"),
)


OPERATION_STATUS = (
    ("MANUAL", "MANUAL"),
    ("AUTO", "AUTO"),
)

CONTRACT = (
    ("AMC", "AMC"),
    ("ON-CALL", "ON-CALL"),
    ("NONE", "NONE"),
)

RATING = (
    ("15", "15"),
    ("20", "20"),
    ("25", "25"),
    ("30", "30"),
    ("35", "35"),
    ("40", "40"),
    ("45", "45"),
    ("50", "50"),
    ("62.5", "62.5"),
    ("75", "75"),
    ("82.5", "82.5"),
    ("100", "100"),
    ("125", "125"),
    ("140", "140"),
    ("160", "160"),
    ("180", "180"),
    ("200", "200"),
    ("225", "225"),
    ("250", "250"),
    ("320", "320"),
    ("365", "365"),
    ("380", "380"),
    ("500", "500"),
    ("625", "625"),
    ("750", "750"),
    ("1000", "1000"),
    ("1500", "1500"),

)

ALTERTYPE = (
    ("energy_output_kva", "energy_output_kva"),
    ("vll_average", "vll_average"),
    ("vlnaverage", "vln_average"),
    ("current_r_phase", "current_r_phase"),
    ("current_y_phase", "current_y_phase"),
    ("current_b_phase", "current_b_phase"),
    ("frequency", "frequency"),
    ("rpm & rpm_ctrl", "rpm & rpm_ctrl"),
    ("Fuel_level_litre", "Fuel_level_litre"),
    ("dg_battery_voltage", "dg_battery_voltage"),
    ("gateway_device_battery", "gateway_device_battery"),
    ("gsm_signal", "gsm_signal"),
    ("room_temperature", "room_temperature"),
)

LIBRARYTYPE = (
    ("Approvals", "Approvals"),
    ("Warranty", "Warranty"),
    ("Test certificate", "Test certificate"),
    ("Service Reports", "Service Reports"),
    ("Quotation", "Quotation"),
    ("Other", "Other")
)


class User(AbstractUser):

    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Login Credential'


class Customer(models.Model):
    User = models.OneToOneField(
        User, on_delete=models.CASCADE, max_length=50)
    Customer_Name = models.CharField(max_length=50)
    Customer_ID = models.CharField(
        max_length=100, unique=True, primary_key=True)
    Customer_Photo = models.ImageField(
        upload_to='pics', default='media/pics/default.png')
    Email_ID = models.EmailField(max_length=50)
    Country = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    City = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Address = models.CharField(max_length=200, blank=True)

    class Meta:
        # db_table = 'Customer Details'
        verbose_name = 'Customer Detail'

    def __str__(self):
        return self.Customer_Name


class Manager (models.Model):
    User = models.ForeignKey(
        User, on_delete=models.CASCADE, max_length=50)
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Manager_Name = models.CharField(max_length=50)
    Manager_Email_ID = models.EmailField(
        max_length=50, unique=True, primary_key=True)
    Mobile_No = models.CharField(max_length=50)
    Contact_No = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.Manager_Name

    class Meta:
        # db_table = 'Manager Details'
        verbose_name = 'Manager Detail'


class User_Detail (models.Model):
    User = models.OneToOneField(
        User, on_delete=models.CASCADE, max_length=50)
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Manager_Name = models.ForeignKey(
        Manager, on_delete=models.CASCADE, max_length=50, blank=True)
    User_Name = models.CharField(max_length=50)
    Contact_Person = models.CharField(max_length=50)
    Email_ID = models.EmailField(max_length=50)
    Contact1 = models.CharField(max_length=50)
    Contact2 = models.CharField(max_length=50, blank=True)
    Device_ID = models.CharField(max_length=50, unique=True, primary_key=True)
    Location = models.CharField(max_length=50, blank=False)
    Country = models.CharField(max_length=50)
    State = models.CharField(max_length=30)
    City = models.CharField(max_length=30)
    Pincode = models.BigIntegerField()
    Address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.Device_ID

    class Meta:
        # db_table = 'User Details'
        verbose_name = 'User Detail'


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


class Asset(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, unique=True, primary_key=True)
    Asset_Name = models.CharField(max_length=50)
    Location = models.CharField(max_length=50)
    Address = models.CharField(max_length=200, blank=True)
    Asset_Photo = models.ImageField(upload_to='pics')
    Diesel_Tank_Size = models.BigIntegerField()
    Rating_In_KVA = models.CharField(max_length=50)
    OEM = models.CharField(max_length=50)
    Seller_Name = models.CharField(max_length=50)
    Warranty_Start_Date = models.DateField(max_length=50)
    Warranty_End_Date = models.DateField(max_length=50)
    Warranty_Period = models.CharField(max_length=50)
    Warranty_Status = models.CharField(
        max_length=20, choices=STATUS, default='YES')
    Date_Of_Installation = models.DateField(max_length=50)
    Commissioning_Date = models.DateField(max_length=50)
    Operations = models.CharField(
        max_length=20, choices=OPERATION_STATUS, default='MANUAL')
    Engine_Make = models.CharField(max_length=50)
    Engine_Model_No = models.CharField(max_length=50)
    Engine_S_NO = models.CharField(max_length=50)
    Engine_Other_Info = models.CharField(max_length=500)
    Alternator_Make = models.CharField(max_length=50)
    Alternator_Model_No = models.CharField(max_length=50)
    Alternator_S_NO = models.CharField(max_length=50)
    Alternator_Other_Info = models.CharField(max_length=500)
    Battery_Make = models.CharField(max_length=50)
    Battery_Model_No = models.CharField(max_length=50)
    Battery_S_NO = models.CharField(max_length=50)
    Battery_Other_Info = models.CharField(max_length=500)
    Battery_Charger_Make = models.CharField(max_length=50)
    Battery_Charger_Model_No = models.CharField(max_length=50)
    Battery_Charger_S_NO = models.CharField(max_length=50)
    Battery_Charger_Other_Info = models.CharField(max_length=500)
    Carpet_Area = models.CharField(max_length=50, default="Null")
    Sanction_Load = models.CharField(max_length=50, default="Null")
    Connected_Load = models.CharField(max_length=50, default="Null")

    class Meta:
        verbose_name = 'DGMS Asset Detail'


class UPS_Asset(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, unique=True, primary_key=True)
    UPS_Rating = models.BigIntegerField()
    UPS_Type = models.CharField(max_length=70)
    Battery_Rating = models.CharField(max_length=200)
    Number_of_batteries = models.BigIntegerField()
    Operating_Volts = models.BigIntegerField()
    OEM = models.CharField(max_length=50)
    Seller_Name = models.CharField(max_length=50)
    UPS_Make = models.CharField(max_length=50)
    UPS_Model_No = models.CharField(max_length=50)
    UPS_Serial_No = models.CharField(max_length=100)
    UPS_Date_Of_Installation = models.DateField()
    UPS_Warranty_Start_Date = models.DateField()
    UPS_Warranty_End_Date = models.DateField()
    UPS_Warranty_Period = models.CharField(max_length=50)
    UPS_Warranty_Status = models.CharField(
        max_length=20, choices=STATUS, default='YES')
    Battery_Make = models.CharField(max_length=50)
    Battery_Model_No = models.CharField(max_length=50)
    Battery_Serial_No = models.CharField(max_length=100)
    Battery_Date_Of_Installation = models.DateField()
    Battery_Warranty_Start_Date = models.DateField()
    Battery_Warranty_End_Date = models.DateField()
    Battery_Warranty_Period = models.CharField(max_length=50)
    Battery_Warranty_Status = models.CharField(
        max_length=20, choices=STATUS, default='YES')
    UPS_EMS_Date_Of_Installation = models.DateField()

    class Meta:
        verbose_name = 'UPS Asset Details'


class EMS_Asset(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, unique=True, primary_key=True)
    Rating_In_KVA = models.BigIntegerField()
    Input_Voltage_Range = models.CharField(max_length=50)
    S_No = models.CharField(max_length=50)
    Cooling = models.CharField(
        max_length=20, choices=COOLING, default='AIR COOLED')
    Oil_Tank_Size = models.CharField(max_length=100, blank=True)
    Other_Info = models.CharField(max_length=100)
    OEM = models.CharField(max_length=50)
    Seller_Name = models.CharField(max_length=50)
    Date_Of_Installation = models.DateField()
    Warranty_Start_Date = models.DateField()
    Warranty_End_Date = models.DateField()
    Warranty_Period = models.CharField(max_length=50)
    Warranty_Status = models.CharField(
        max_length=20, choices=STATUS, default='YES')
    EMS_Date_Of_Installation = models.DateField()
    Other_Info_new = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'EMS Asset Details'


class Service_History(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, primary_key=True)
    Service_Contract = models.CharField(
        max_length=20, choices=CONTRACT, default='AMC')
    Service_Document = models.FileField(blank=True)
    Service_Provider = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Contact = models.CharField(max_length=20)
    Email = models.CharField(max_length=50, default="info@emot.co.in")
    Last_Service_Date = models.DateField(max_length=50)
    Activity = models.CharField(max_length=300)
    Remark = models.CharField(max_length=300)
    Activity1 = models.CharField(max_length=300, default="NULL")
    Remark1 = models.CharField(max_length=300, default="NULL")
    Next_Service_Date = models.DateField()
    Battery_Next_Replacement_Date = models.DateField(blank=True)
    Battery_Last_Replacement_Date = models.DateField(blank=True)

    class Meta:
        verbose_name = 'DGMS Service Detail'


class UPS_Service_History(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, primary_key=True, unique=True)
    Service_Contract = models.CharField(
        max_length=20, choices=CONTRACT, default='AMC')
    Service_Provider = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Contact = models.CharField(max_length=20)
    Email = models.CharField(max_length=50, default="info@emot.co.in")
    Battery_Last_Replaced_Date = models.DateField(max_length=50)
    Battery_Next_Replacment_Date = models.DateField(max_length=50)
    Last_Service_Date = models.DateField(max_length=50)
    Activity = models.CharField(max_length=300)
    Remark = models.CharField(max_length=300)
    Activity1 = models.CharField(max_length=300, default="NULL")
    Remark1 = models.CharField(max_length=300, default="NULL")
    Next_Service_Date = models.DateField(max_length=50)

    class Meta:
        verbose_name = 'UPS Service History'


class EMS_Service_History(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, primary_key=True, unique=True)
    Service_Contract = models.CharField(
        max_length=20, choices=CONTRACT, default='AMC')
    Service_Provider = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    Contact = models.CharField(max_length=20)
    Email = models.CharField(max_length=50, default="info@emot.co.in")
    Last_Service_Date = models.DateField()
    Activity = models.CharField(max_length=300)
    Remark = models.CharField(max_length=300)
    Activity1 = models.CharField(max_length=300, default="NULL")
    Remark1 = models.CharField(max_length=300, default="NULL")
    Next_Service_Date = models.DateField()

    class Meta:
        verbose_name = 'EMS Service History'


class DGMS_Device_Info(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, primary_key=True, unique=True)
    DGMS_Date_Of_Installation = models.DateField(max_length=50)
    Version = models.CharField(max_length=50)
    Device_Serial_No = models.CharField(max_length=50)
    Sim_Card = models.CharField(max_length=50)
    IMEI_No = models.CharField(max_length=100)
    Other = models.CharField(max_length=200)
    Other_Info = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'DGMS Device Info'


class Sensor_Info(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, primary_key=True, unique=True)
    Energy_Meter_Make_Info = models.CharField(max_length=50)
    Energy_Meter_Model_No = models.CharField(max_length=50)
    Energy_Meter_S_No = models.CharField(max_length=50)
    Current_Transformer_Make_Info = models.CharField(max_length=50)
    Current_Transformer_Model_No = models.CharField(max_length=50)
    Current_Transformer_S_No = models.CharField(max_length=50)
    Current_Transformer_CT_Ratio = models.CharField(max_length=50)
    Fuel_Sensor_Make_Info = models.CharField(max_length=50)
    Fuel_Sensor_Model_No = models.CharField(max_length=50)
    Fuel_SensorS_No = models.CharField(max_length=50)
    Fuel_Sensor_Length = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'DGMS Sensor Info'


class Before_DGMA_INSTALLATION(models.Model):
    Customer_Name = models.ForeignKey(
        Customer, on_delete=models.CASCADE, max_length=50)
    Device_ID = models.OneToOneField(
        User_Detail, on_delete=models.CASCADE, max_length=50, primary_key=True, unique=True)
    Previous_Run_Hour = models.CharField(max_length=50)
    Previous_Fuel_Consumed = models.CharField(max_length=50)
    Run_Count = models.CharField(max_length=50)
    Units_Generated = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'DGMS Before Installation Information'


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
    device_tank_size = models.BigIntegerField(blank=True, null=True)
    device_state = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class DevicesInfo(models.Model):
    # id = models.AutoField()
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
    run_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_operational'


class Price(models.Model):

    Location = models.CharField(primary_key=True, max_length=50)
    Energy_Price = models.CharField(max_length=50)
    Diesel_Price = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Fuel & Energy Price'


class DeviceCounterView(models.Model):
    device_id = models.CharField(max_length=20, primary_key=True)
    counter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_counter_view'


class FuelFilledReport(models.Model):
    device_time = models.DateTimeField(primary_key=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    fuel_level = models.IntegerField(blank=True, null=True)
    fuel_added = models.IntegerField(blank=True, null=True)
    new_fuel_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fuel_capacity_per_mm_based_check'


class OperationalPerformanceReport(models.Model):
    account_name = models.CharField(max_length=200, blank=True, null=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    start_time = models.DateTimeField(primary_key=True)
    end_time = models.DateTimeField(blank=True, null=True)
    fuel_level = models.FloatField(blank=True, null=True)
    unit_generated_kwh = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    fuel_consumed = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    energy_generated_kwh = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    carbon_footprint = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    fuel_cost = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    per_unit_cost = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    run_hours = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    maximum_demand_load = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    efficiency = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    device_location = models.CharField(max_length=200, blank=True, null=True)
    device_rating = models.FloatField(blank=True, null=True)
    device_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operational_performance_report'


class SetAlert(models.Model):
    KVA_Rating = models.BigIntegerField(choices=RATING, default='15')
    Alert = models.CharField(
        max_length=50, choices=ALTERTYPE, default='energy_output_kw')
    Less_Than = models.CharField(max_length=30, blank=False)
    More_Than = models.CharField(max_length=30, blank=False)


class Automation(models.Model):
    Device_ID = models.CharField(max_length=30, blank=False)
    Status = models.CharField(max_length=30, blank=False)
    Start_Time = models.DateTimeField()
    End_Time = models.DateTimeField()
    Button = models.CharField(max_length=30, blank=True)


class ThresholdDetails(models.Model):
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
    rating = models.FloatField()
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
    device_phase = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'threshold_metadata'


class ThresholdMetadataOld(models.Model):
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
    device_phase = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'threshold_metadata_old'
        unique_together = (('rating', 'threshold_operator'),
                           ('rating', 'threshold_operator'),)


class Library(models.Model):
    Device_ID = models.ForeignKey(User_Detail, on_delete=models.CASCADE)
    Type = models.CharField(
        max_length=20, choices=LIBRARYTYPE, default='Other')
    File = models.FileField(blank=True)
    Date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'DGMS Library'
