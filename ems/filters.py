from urllib import request
import requests
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

# status = ['power_factor', 'gateway_device_battery', 'fuel_level_percentage', 'gsm_signal', 'energy_output_kw_total', 'dg_battery_voltage', 'room_temperature', 'frequency',
#           'rpm_ctrl', 'current_b_phase', 'vll_average', 'energy_output_kva', 'current_r_phase', 'rpm', 'current_y_phase', ]


class DateInput(forms.DateInput):
    input_type = 'date'


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
        exclude = ['device_id', 'start_time', 'end_time', 'fuel_level', 'unit_generated_kwh', 'fuel_consumed', 'energy_generated_kwh',
                   'carbon_footprint', 'fuel_cost', 'per_unit_cost', 'run_hours', 'maximum_demand_load', 'efficiency', 'created_at', 'updated_at', ]


class AlertFilter(django_filters.FilterSet):
    alert_level = django_filters.ChoiceFilter(
        choices=ALTER_CHOICES, label='', field_name='alert_level',   lookup_expr='iexact', empty_label="Alert Level",)

    # alert_open = django_filters.ChoiceFilter(
    #     choices=ALTERSTATUS_CHOICES, label='', field_name='alert_open',   lookup_expr='iexact')

    device_id = django_filters.ChoiceFilter(
        choices=[[u.device_id,  u.device_id] for u in LoginUserDetail.objects.all()], field_name='device_id', lookup_expr='icontains', label='', empty_label="Device ID",)

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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     request = kwargs['request']
    #     if request.user.is_authenticated:
    #         username = request.user.username
    #         my_choices = [[u.Device_ID,  u.Device_ID]
    #                       for u in User_Detail.objects.filter(Customer_Name=username)]
    #         self.filters['device_id'].extra.update({'choices': my_choices})


class DeviceAlertFilter(django_filters.FilterSet):
    alert_level = django_filters.ChoiceFilter(
        choices=ALTER_CHOICES, label='', field_name='alert_level',   lookup_expr='iexact', empty_label="Alter Level",)

    # alert_open = django_filters.ChoiceFilter(
    #     choices=ALTERSTATUS_CHOICES, label='', field_name='alert_open',   lookup_expr='iexact')

    # device_id = django_filters.ChoiceFilter(choices=[[u.Device_ID,  u.Device_ID] for u in User_Detail.objects.all(
    # )], field_name='device_id', lookup_expr='icontains', label='')

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
