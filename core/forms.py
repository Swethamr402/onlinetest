from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models as core_models

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = core_models.Employee
        fields = ['employee_id', 'first_name', 'last_name', 'designation', 'is_active']

class EmployeeRegistrationForm(UserCreationForm):
    class Meta:
        model = core_models.UserProfile
        fields = ('username', 'mobile', 'first_name', 'last_name', 'email','business_unit','team','password1', 'password2')
