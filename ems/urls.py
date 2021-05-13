from django.urls import path
from . import views

urlpatterns = [
    path('', views.ems, name='ems'),
    path('/<slug:device_id>/emsDashboard',
         views.emsDashboard, name='emsDashboard')
]
