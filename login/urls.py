from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/', views.automation, name='automation'),
    path('login', views.login, name='login'),
    path('login1', views.login1, name='login1'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logoutUser',
         views.logoutUser, name='logoutUser'),
    path('/<slug:device_id>/asset', views.asset, name='asset'),
    path('alert', views.alert, name='alert'),
    path('/<slug:device_id>/dgmsDashboard',
         views.dgmsDashboard, name='dgmsDashboard'),
    path('/<slug:device_id>/servicehistory/',
         views.servicehistory, name='servicehistory'),
    path('/<slug:device_id>/energyPara', views.energyPara, name='energyPara'),
    path('/<slug:device_id>/loadKPI', views.loadKPI, name='loadKPI'),
    path('/<slug:device_id>/enginePara', views.enginePara, name='enginePara'),
    path('/<slug:device_id>/performanceKPI',
         views.performanceKPI, name='performanceKPI'),
    path('/<slug:device_id>/deviceInfoKPI',
         views.deviceInfoKPI, name='deviceInfoKPI'),
    path('/<slug:device_id>/fuel_report',
         views.fuel_report, name='fuel_report'),
    path('/<slug:device_id>/operational_report',
         views.operational_report, name='operational_report'),
    path('/<slug:device_id>/performance_report',
         views.performance_report, name='performance_report'),
    path('/<slug:device_id>/asset_library',
         views.asset_library, name='asset_library'),
    path('/<slug:device_id>/customer', views.customer, name='customer'),
    path('/<slug:device_id>/device_alert',
         views.device_alert, name='device_alert'),
    path('customerInfo', views.customerInfo, name='customerInfo'),
    path('/<slug:location>/updateprice', views.updateprice, name='updateprice'),
    #     path('assetTable', views.assetTable, name='assetTable'),
    #     path('addCustomer', views.addCustomer, name='addCustomer'),
    #     path('addManager', views.addManager, name='addManager'),
    #     path('addUser', views.addUser, name='addUser'),
    #     path('assetInfo', views.assetInfo, name='assetInfo'),
    #     path('deviceInfo', views.deviceInfo, name='deviceInfo'),
    #     path('sensorInfo', views.sensorInfo, name='sensorInfo'),
    #     path('addService_history', views.addService_history, name='addService_history'),
    #     path('beforedgms_installation', views.beforedgms_installation,
    #          name='beforedgms_installation'),
    path('update', views.update, name='update'),
    #     path('setAlert', views.setAlert, name='setAlert'),
    path('reset_password',
         auth_views.PasswordResetView.as_view(
             template_name="password_reset_form.html"),
         name="reset_password"),

    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset_done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset_form1.html"),
         name="password_reset_confirm"),

    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_complete.html"),
         name="password_reset_complete"),

    path('change_password',
         auth_views.PasswordChangeView.as_view(
             template_name="password_change.html"),
         name="password_change"),

    path('password_change_done',
         auth_views.PasswordChangeView.as_view(
             template_name="password_change_done.html"),
         name="password_change_done"),


]
