from django.urls import path
from . import views

urlpatterns = [
    path('', views.ems, name='ems'),
    path('/<slug:device_id>/emsDashboard',
         views.emsDashboard, name='emsDashboard'),
    path('/<slug:device_id>/asset', views.emsasset_detail, name='emsasset_detail'),
    path('/alert', views.emsalert, name='emsalert'),
    path('/<slug:device_id>/servicehistory/',
         views.emsservice_history, name='emsservice_history'),
    path('/<slug:device_id>/loadKPI', views.emsLoadKPI, name='emsLoadKPI'),
    path('/<slug:device_id>/EnergParaKPI',
         views.emsEnergyPara, name='emsEnergyPara'),
    path('/<slug:device_id>/deviceInfoKPI',
         views.emsDeviceInfoKPI, name='emsDeviceInfoKPI'),
    path('/<slug:device_id>/device_alert',
         views.emsdevice_alert, name='emsdevice_alert'),
]
