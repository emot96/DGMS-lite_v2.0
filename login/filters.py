from .models import *
import django_filters
from django_filters import DateFilter
from django import forms


# def alert(request):
#     username = None
#     email = None
#     usertype = None
#     if request.user.is_customer:
#         Customer_Name = Customer.objects.get(
#             Customer_Name=username).Customer_Name
#         Customer_ID = Customer.objects.get(
#             Customer_Name=username).Customer_ID
#         Total = Device.objects.filter(account_id=Customer_ID).count()
#         Device_ID = Device.objects.filter(account_id=Customer_ID)
#         DeviceID = []
#         for i in range(Total):
#             a = Device_ID[i].device_id
#             DeviceID.append(a)


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
)

ALTERSTATUS_CHOICES = (
    (True, 'Active'),
    (False, 'Resolved'),
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
    start_date = django_filters.DateFilter(label='Start Date', field_name='device_time', lookup_expr='gt',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='device_time', lookup_expr='lt',
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


class OperationalReportFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Start Date', field_name='start_time', lookup_expr='gt',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='end_time', lookup_expr='lt',
                                         widget=DateInput(
                                             attrs={
                                                 'class': 'datepicker'
                                             }
                                         )
                                         )

    class Meta:
        model = OperationalPerformanceReport
        fields = "__all__"
        exclude = ['account_name', 'device_id', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh', 'carbon_footprint',
                   'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'device_location', 'device_rating', 'device_status']


class PerformanceReportFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Start Date', field_name='start_time', lookup_expr='gt',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='end_time', lookup_expr='lt',
                                         widget=DateInput(
                                             attrs={
                                                 'class': 'datepicker'
                                             }
                                         )
                                         )

    class Meta:
        model = OperationalPerformanceReport
        fields = "__all__"
        exclude = ['account_name', 'device_id', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh', 'carbon_footprint',
                   'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'device_location', 'device_rating', 'device_status']


class KPIFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(label='Start Date', field_name='device_time', lookup_expr='gt',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='device_time', lookup_expr='lt',
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
    start_date = django_filters.DateFilter(label='Start Date', field_name='start_time', lookup_expr='gt',
                                           widget=DateInput(
                                               attrs={
                                                   'class': 'datepicker'
                                               }
                                           )
                                           )
    end_date = django_filters.DateFilter(label='End Date', field_name='end_time', lookup_expr='lt',
                                         widget=DateInput(
                                             attrs={
                                                 'class': 'datepicker'
                                             }
                                         )
                                         )

    class Meta:
        model = DeviceOperational
        fields = "__all__"
        exclude = ['device_id', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh',
                   'carbon_footprint', 'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'created_at', 'updated_at', ]


class AlertFilter(django_filters.FilterSet):
    alert_level = django_filters.ChoiceFilter(
        choices=ALTER_CHOICES, label='', field_name='alert_level',   lookup_expr='iexact')

    # alert_open = django_filters.ChoiceFilter(
    #     choices=ALTERSTATUS_CHOICES, label='', field_name='alert_open',   lookup_expr='iexact')

    device_id = django_filters.ChoiceFilter(choices=[[u.Device_ID,  u.Device_ID] for u in User_Detail.objects.all(
    )], field_name='device_id', lookup_expr='icontains', label='')

    alert_type_name = django_filters.ChoiceFilter(
        choices=FILTER_CHOICES, label='', field_name='alert_type_name',   lookup_expr='iexact')

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


class DeviceAlertFilter(django_filters.FilterSet):
    alert_level = django_filters.ChoiceFilter(
        choices=ALTER_CHOICES, label='', field_name='alert_level',   lookup_expr='iexact')

    # alert_open = django_filters.ChoiceFilter(
    #     choices=ALTERSTATUS_CHOICES, label='', field_name='alert_open',   lookup_expr='iexact')

    # device_id = django_filters.ChoiceFilter(choices=[[u.Device_ID,  u.Device_ID] for u in User_Detail.objects.all(
    # )], field_name='device_id', lookup_expr='icontains', label='')

    alert_type_name = django_filters.ChoiceFilter(
        choices=FILTER_CHOICES, label='', field_name='alert_type_name',   lookup_expr='iexact')

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
