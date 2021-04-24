from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from django.db.models import fields
from .models import *
from django.forms import ModelForm, widgets
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = "__all__"


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = "__all__"


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = "__all__"

        widgets = {
            'Location': forms.TextInput(attrs={'class': 'row'}),
            'Energy_Price': forms.TextInput(attrs={'class': 'row'}),
            'Diesel_Price': forms.TextInput(attrs={'class': 'row'}),

        }









