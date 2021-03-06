# #from emot.login.models import Customer, Manager_, User_
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(UserAdmin):
    model = User
    add_form = UserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': (
                    'is_customer',
                    'is_manager',
                    'is_user'
                )
            }
        )
    )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Customer_ID', 'Email_ID')
    # search_fields = ('Customer_Name', 'Customer_ID', 'Email_ID')
    ordering = ['Customer_Name', 'Customer_ID']


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('Manager_Name', 'Customer_Name', 'Manager_Email_ID')
    # search_fields = ('Manager_Name', 'Customer_ID', 'Manager_Email_ID')
    ordering = ['Manager_Name', 'Customer_Name']


class User_DetailAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Manager_Name',
                    'User_Name', 'Device_ID')
    # search_fields = ('Customer_ID', 'Manager_Email_ID',
    #                  'User_Name', 'Device_ID')
    ordering = ['Customer_Name', 'Manager_Name', 'User_Name', 'Device_ID']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID', 'Asset_Name')
    ordering = ['Customer_Name', 'Device_ID', 'Asset_Name']


class Service_HistoryAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID', 'Service_Provider')
    ordering = ['Customer_Name', 'Device_ID', 'Service_Provider']


class DGMS_Device_InfoAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID')
    ordering = ['Customer_Name', 'Device_ID']


class Sensor_InfoAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID')
    ordering = ['Customer_Name', 'Device_ID']


class Before_DGMA_INSTALLATIONAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID')
    ordering = ['Customer_Name', 'Device_ID']


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'account_name',
                    'account_email', 'account_addr')
    ordering = ['account_id', 'account_name', 'account_email', 'account_addr']


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'device_name',
                    'account_id', 'device_location')
    ordering = ['device_id', 'device_name', 'account_id', 'device_location']


class DeviceOperationalAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'unit_generated_kwh', 'energy_generated_kwh')
    ordering = ['device_id', 'unit_generated_kwh', 'energy_generated_kwh']


class PriceAdmin(admin.ModelAdmin):
    list_display = ('Location', 'Energy_Price', 'Diesel_Price')
    ordering = ['Location', 'Energy_Price', 'Diesel_Price']


class EMS_AssetAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID', 'Rating_In_KVA')
    ordering = ['Customer_Name', 'Device_ID', 'Rating_In_KVA']


class EMS_Service_HistoryAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID', 'Service_Provider')
    ordering = ['Customer_Name', 'Device_ID', 'Service_Provider']


class UPS_AssetAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID', 'UPS_Rating')
    ordering = ['Customer_Name', 'Device_ID', 'UPS_Rating']


class UPS_Service_HistoryAdmin(admin.ModelAdmin):
    list_display = ('Customer_Name', 'Device_ID', 'Service_Provider')
    ordering = ['Customer_Name', 'Device_ID', 'Service_Provider']


class ThresholdMetadataAdmin(admin.ModelAdmin):
    list_display = ('rating', 'threshold_operator', 'device_phase')
    ordering = ['rating', 'threshold_operator', 'device_phase']


class LibraryAdmin(admin.ModelAdmin):
    list_display = ('Device_ID', 'Type', 'File')
    ordering = ['Device_ID', 'Type', 'File']


# # # Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(User_Detail,  User_DetailAdmin)
admin.site.register(Accounts, AccountsAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Service_History, Service_HistoryAdmin)
admin.site.register(DGMS_Device_Info, DGMS_Device_InfoAdmin)
admin.site.register(Sensor_Info, Sensor_InfoAdmin)
admin.site.register(Before_DGMA_INSTALLATION, Before_DGMA_INSTALLATIONAdmin)

admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceOperational, DeviceOperationalAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(EMS_Asset, EMS_AssetAdmin)
admin.site.register(EMS_Service_History, EMS_Service_HistoryAdmin)
admin.site.register(UPS_Asset, UPS_AssetAdmin)
admin.site.register(UPS_Service_History, UPS_Service_HistoryAdmin)
admin.site.register(Automation)
admin.site.register(ThresholdMetadata, ThresholdMetadataAdmin)
admin.site.register(Library, LibraryAdmin)
