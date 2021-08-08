from urllib import request
# import urllib.request
from django.db import reset_queries
from django.db.models import fields
from .models import *
import django_filters
from django_filters import DateFilter
from django import forms


FILTER_CHOICES = (
    ('power_factor', 'power_factor'),
    ('gateway_device_battery', 'gateway_device_battery'),
    ('fuel_level_percentage', 'fuel_level_percentage'),
    ('gsm_signal', 'gsm_signal'),
    ('energy_output_kw_total', 'energy_output_kw_total'),
    ('dg_battery_voltage', 'dg_battery_voltage'),
    ('room_temperature', 'room_temperature'),
    ('frequency', 'frequency'),
    ('rpm_ctrl', 'rpm_ctrl'),
    ('current_b_phase', 'current_b_phase'),
    ('vll_average', 'vll_average'),
    ('energy_output_kva', 'energy_output_kva'),
    ('current_r_phase', 'current_r_phase'),
    ('rpm', 'rpm'),
    ('current_y_phase', 'current_y_phase'),

)

ALTER_CHOICES = (
    ('Y', 'Warning'),
    ('R', 'Critical'),
    ('V', 'Rule Based'),
)

ALTERSTATUS_CHOICES = (
    (True, 'Active'),
    (False, 'Resolved'),
)

STATUS = (
    ('ON', 'ON'),
    ('OFF', 'OFF'),
)

LIBRARYTYPE = (
    ("Approvals", "Approvals"),
    ("Warranty", "Warranty"),
    ("Test certificate", "Test certificate"),
    ("Service Reports", "Service Reports"),
    ("Quotation", "Quotation"),
    ("Other", "Other")
)
# status = ['power_factor', 'gateway_device_battery', 'fuel_level_percentage', 'gsm_signal', 'energy_output_kw_total', 'dg_battery_voltage', 'room_temperature', 'frequency',
#           'rpm_ctrl', 'current_b_phase', 'vll_average', 'energy_output_kva', 'current_r_phase', 'rpm', 'current_y_phase', ]


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomerFilter(django_filters.FilterSet):
    User = django_filters.ChoiceFilter(choices=[[u.User_Name,  u.User_Name] for u in User_Detail.objects.all(
    )], field_name='User_Name', lookup_expr='icontains', label='')
    Device_ID = django_filters.ChoiceFilter(choices=[[u.Device_ID,  u.Device_ID] for u in User_Detail.objects.all(
    )], field_name='Device_ID', lookup_expr='icontains', label='')
    User = django_filters.ChoiceFilter(choices=[[u.User_Name,  u.User_Name] for u in User_Detail.objects.all(
    )], field_name='User_Name', lookup_expr='icontains', label='')
    Country = django_filters.ChoiceFilter(choices=[[u.Country,  u.Country] for u in User_Detail.objects.all(
    ).distinct('Country')], field_name='Country', lookup_expr='icontains', label='')
    State = django_filters.ChoiceFilter(choices=[[u.State,  u.State] for u in User_Detail.objects.all(
    ).distinct('State')], field_name='State', lookup_expr='icontains', label='')
    City = django_filters.ChoiceFilter(choices=[[u.City,  u.City] for u in User_Detail.objects.all(
    ).distinct('City')], field_name='City', lookup_expr='icontains', label='')

    class Meta:
        model = User_Detail
        fields = "__all__"
        exclude = ['User', 'Customer_Name', 'Contact_Person', 'Manager_Name', 'Email_ID', 'User_Name',
                   'Device_ID', 'Country', 'State', 'City', 'Contact1', 'Contact2', 'Location', 'Pincode', 'Address']


class FuelFilledReportFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Start Date', field_name='device_time', lookup_expr='date__gte',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='device_time', lookup_expr='date__lte',
                                         widget=DateInput(
                                             attrs={
                                                 'class': 'datepicker'
                                             }
                                         )
                                         )

    class Meta:
        model = FuelFilledReport
        fields = "__all__"
        exclude = ['device_time', 'device_id', 'fuel_level', 'fuel_added',
                   'fuel_consumed', 'new_fuel_level', ]


# class OperationalReportFilter(django_filters.FilterSet):
#     start_date = django_filters.DateFilter(label='Start Date', field_name='start_time', lookup_expr='date__gte',
#                                            widget=DateInput(
#                                                attrs={
#                                                    'class': 'datepicker'
#                                                }
#                                            )
#                                            )
#     end_date = django_filters.DateFilter(label='End Date', field_name='end_time', lookup_expr='date__lte',
#                                          widget=DateInput(
#                                              attrs={
#                                                  'class': 'datepicker'
#                                              }
#                                          )
#                                          )

#     class Meta:
#         model = OperationalPerformanceReport
#         fields = "__all__"
#         exclude = ['account_name', 'device_id', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh', 'carbon_footprint',
#                    'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'device_location', 'device_rating', 'device_status']


# class PerformanceReportFilter(django_filters.FilterSet):
#     start_date = django_filters.DateFilter(label='Start Date', field_name='start_time', lookup_expr='date__gte',
#                                            widget=DateInput(
#                                                attrs={
#                                                    'class': 'datepicker'
#                                                }
#                                            )
#                                            )
#     end_date = django_filters.DateFilter(label='End Date', field_name='end_time', lookup_expr='date__lte',
#                                          widget=DateInput(
#                                              attrs={
#                                                  'class': 'datepicker'
#                                              }
#                                          )
#                                          )

#     class Meta:
#         model = OperationalPerformanceReport
#         fields = "__all__"
#         exclude = ['account_name', 'device_id', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh', 'carbon_footprint',
#                    'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'device_location', 'device_rating', 'device_status']


class KPIFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Start Date', field_name='device_time', lookup_expr='date__gte',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='device_time', lookup_expr='date__lte',
                                         widget=DateInput(
                                             attrs={
                                                 'class': 'datepicker'
                                             }
                                         )
                                         )

    class Meta:
        model = DevicesInfo
        fields = "__all__"
        exclude = ['device_header', 'device_id', 'device_time', 'gateway_device_battery', 'room_temperature', 'dg_battery_voltage', 'gateway_power_status',
                   'gsm_signal',
                   'energy_output_kw_total',
                   'kva_r_phase',
                   'kva_y_phase',
                   'kva_b_phase',
                   'power_factor',
                   'energy_output_kva',
                   'vll_average',
                   'vry_phase_voltage',
                   'vyb_phase_voltage',
                   'vbr_phase_voltage',
                   'vln_average',
                   'vr_phase_voltage',
                   'vy_phase_voltage',
                   'vb_phase_voltage',
                   'current_average',
                   'current_r_phase',
                   'current_y_phase',
                   'current_b_phase',
                   'frequency',
                   'unit_generated_kwh',
                   'rpm',
                   'dg_runtime_seconds',
                   'fuel_level_percentage',
                   'fuel_level_litre',
                   'fuel_level_volt',
                   'fuel_level_mm',
                   'rpm_ctrl',
                   'dg_counter_ctrl',
                   'runtime_second_ctrl',
                   'device_status',
                   'created_at',
                   'updated_at',
                   ]


class DeviceOperationalFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Start Date', field_name='start_time', lookup_expr='date__gte',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='end_time', lookup_expr='date__lte',
                                         widget=DateInput(
                                             attrs={
                                                 'class': 'datepicker'
                                             }
                                         )
                                         )

    class Meta:
        model = DeviceOperational
        fields = "__all__"
        exclude = ['device_id', 'run_count', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh',
                   'carbon_footprint', 'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'created_at', 'updated_at', ]


class AlertFilter(django_filters.FilterSet):
    alert_level = django_filters.ChoiceFilter(
        choices=ALTER_CHOICES, label='', field_name='alert_level',   lookup_expr='iexact', empty_label="Alert Level",)

    device_id = django_filters.ChoiceFilter(
        choices=None, field_name='device_id', lookup_expr='icontains', label='', empty_label="Device ID",)

    alert_type_name = django_filters.ChoiceFilter(
        choices=FILTER_CHOICES, label='', field_name='alert_type_name',   lookup_expr='iexact', empty_label="Alert Name",)

    created_at = django_filters.DateFilter(label='Start Date', field_name='created_at', lookup_expr='date__gte',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )

    updated_at = django_filters.DateFilter(label='End Date', field_name='updated_at', lookup_expr='date__lte',
                                           widget=DateInput(
                                               attrs={
                                                 'class': 'datepicker'
                                               }
                                           )
                                           )

    class Meta:
        model = Alerts
        fields = "__all__"
        exclude = ['alert_id', 'alert_type_name', 'device_id', 'alert_open', 'alert_level', 'param_value',
                   'param_threshold_value', 'created_at', 'updated_at', ]

    def __init__(self, *args, **kwargs):
        super(AlertFilter, self).__init__(*args, **kwargs)
        request = kwargs['request']
        if request.user.is_authenticated:
            username = request.user.username
            if request.user.is_customer:
                Customer_Name = Customer.objects.get(
                    Customer_Name=username).Customer_Name
                Customer_ID = Customer.objects.get(
                    Customer_Name=username).Customer_ID
                my_deviceid = [[u.device_id,  u.device_id]
                               for u in Device.objects.filter(account_id=Customer_ID).distinct()]

            elif request.user.is_manager:
                Customer_Name = Manager.objects.get(
                    Manager_Name=username).Customer_Name
                managername = Manager.objects.get(
                    Manager_Name=username).Manager_Name
                User_details = User_Detail.objects.all()
                DeviceID = []
                for det in User_details:
                    if str(det.Manager_Name) == managername:
                        DeviceID.append(det.Device_ID)
                my_deviceid = [[u.device_id,  u.device_id]
                               for u in Device.objects.filter(device_id__in=DeviceID).distinct()]

            self.filters['device_id'].extra.update(
                {'choices': my_deviceid})


class DeviceAlertFilter(django_filters.FilterSet):
    alert_level = django_filters.ChoiceFilter(
        choices=ALTER_CHOICES, label='', field_name='alert_level',   lookup_expr='iexact', empty_label="Alter Level",)

    alert_type_name = django_filters.ChoiceFilter(
        choices=FILTER_CHOICES, label='', field_name='alert_type_name',   lookup_expr='iexact', empty_label="Alter Type",)

    created_at = django_filters.DateFilter(label='Start Date', field_name='created_at', lookup_expr='gt',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )

    updated_at = django_filters.DateFilter(label='End Date', field_name='updated_at', lookup_expr='lt',
                                           widget=DateInput(
                                               attrs={
                                                 'class': 'datepicker'
                                               }
                                           )
                                           )

    class Meta:
        model = Alerts
        fields = "__all__"
        exclude = ['alert_id', 'alert_type_name', 'device_id', 'alert_open', 'alert_level', 'param_value',
                   'param_threshold_value', 'created_at', 'updated_at', ]


class DashboardFilter(django_filters.FilterSet):

    device_state = django_filters.ChoiceFilter(
        choices=None, label='', field_name='device_state',   lookup_expr='iexact', empty_label="State")

    device_location = django_filters.ChoiceFilter(
        choices=None, field_name='device_location', lookup_expr='iexact', label='', empty_label="Location")

    device_status = django_filters.ChoiceFilter(
        choices=STATUS, label='', field_name='device_status',   lookup_expr='iexact', empty_label="Status")

    device_id = django_filters.ChoiceFilter(
        choices=None, field_name='device_id', lookup_expr='iexact', label='', empty_label="ID")

    device_rating = django_filters.ChoiceFilter(
        choices=None, field_name='device_rating', lookup_expr='icontains', label='', empty_label="Rating")

    class Meta:
        models = Device
        fields = "__all__"
        exclude = ["device_name", "device_desc", "device_type", "account_id",
                   "device_created_at", "device_updated_at", "fuel_report_link", "operational_report_link"]

    def __init__(self, *args, **kwargs):
        super(DashboardFilter, self).__init__(*args, **kwargs)
        request = kwargs['request']
        if request.user.is_authenticated:
            username = request.user.username
            if request.user.is_customer:
                Customer_Name = Customer.objects.get(
                    Customer_Name=username).Customer_Name
                Customer_ID = Customer.objects.get(
                    Customer_Name=username).Customer_ID

                my_deviceid = [[u.device_id,  u.device_id]
                               for u in Device.objects.filter(account_id=Customer_ID).distinct()]
                my_device_rating = [[u.device_rating,  u.device_rating]
                                    for u in Device.objects.distinct("device_rating").filter(account_id=Customer_ID)]

                my_device_location = [[u.device_location,  u.device_location] for u in Device.objects.distinct(
                    "device_location").filter(account_id=Customer_ID)]

                my_device_state = [[u.device_state,  u.device_state] for u in Device.objects.distinct(
                    "device_state").filter(account_id=Customer_ID)]
            elif request.user.is_manager:
                Customer_Name = Manager.objects.get(
                    Manager_Name=username).Customer_Name
                managername = Manager.objects.get(
                    Manager_Name=username).Manager_Name
                User_details = User_Detail.objects.all()
                DeviceID = []
                for det in User_details:
                    if str(det.Manager_Name) == managername:
                        DeviceID.append(det.Device_ID)

                my_deviceid = [[u.device_id,  u.device_id]
                               for u in Device.objects.filter(device_id__in=DeviceID).distinct()]
                my_device_rating = [[u.device_rating,  u.device_rating]
                                    for u in Device.objects.distinct("device_rating").filter(device_id__in=DeviceID)]

                my_device_location = [[u.device_location,  u.device_location] for u in Device.objects.distinct(
                    "device_location").filter(device_id__in=DeviceID)]

                my_device_state = [[u.device_state,  u.device_state] for u in Device.objects.distinct(
                    "device_state").filter(device_id__in=DeviceID)]

            self.filters['device_id'].extra.update({'choices': my_deviceid})
            self.filters['device_rating'].extra.update(
                {'choices': my_device_rating})
            self.filters['device_location'].extra.update(
                {'choices': my_device_location})
            self.filters['device_state'].extra.update(
                {'choices': my_device_state})


class LibraryFilter(django_filters.FilterSet):
    file_type = django_filters.ChoiceFilter(
        choices=LIBRARYTYPE, label='', field_name='Type',   lookup_expr='iexact', empty_label="File Type",)

    class Meta:
        model = Library
        fields = "__all__"
        exclude = ['Device_ID', 'Type', 'File', 'Date']
