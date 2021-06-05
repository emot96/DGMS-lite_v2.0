from django.urls import path
from . import views

urlpatterns = [
    path('', views.ups, name='ups'),
    path('/<slug:device_id>/upsDashboard',
         views.upsDashboard, name='upsDashboard'),
    path('/<slug:device_id>/asset', views.upsasset_detail, name='upsasset_detail'),
    path('/alert', views.upsalert, name='upsalert'),
    path('/<slug:device_id>/servicehistory/',
         views.upsservice_history, name='upsservice_history'),
    path('/<slug:device_id>/loadKPI', views.upsLoadKPI, name='upsLoadKPI'),
    path('/<slug:device_id>/EnergParaKPI',
         views.upsEnergyPara, name='upsEnergyPara'),
    path('/<slug:device_id>/deviceInfoKPI',
         views.upsDeviceInfoKPI, name='upsDeviceInfoKPI'),
    path('/<slug:device_id>/device_alert',
         views.upsdevice_alert, name='upsdevice_alert'),
    path('/<slug:device_id>/operational_report',
         views.upsoperational_report, name='upsoperational_report'),
]
