from django.db.models import fields
from rest_framework import serializers
from .models import *


class AutomationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automation
        fields = '__all__'
