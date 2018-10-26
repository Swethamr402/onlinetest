# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from datetime import datetime
from django import forms
from django.core.validators import validate_email
from . import models as core_models
from . import forms as core_forms

from django.core.validators import EmailValidator, URLValidator
# from django.db.models.loading import get_model
from django.forms import ValidationError

from django.utils.translation import ugettext as _
from django.forms import EmailField
from django.core.exceptions import ValidationError
from django.contrib import messages

from . import models as quiz_models
# Create your views here.

# @login_required
# def home(request):
#     return render(request, 'core/home.html')

@login_required
def home(request):
    return render(request, 'core/home.html')



@login_required
def dashboard(request,quiz_id):
        return render(request, 'core/dashboard.html')


    # return render(request, 'core/dashboard.html')

@login_required
def list_employees(request):
    employees = core_models.Employee.objects.all()
    return render(request, 'core/list_employees.html', {
    'employees': employees
    })

@login_required
def view_employee(request, employee_id):
    doctor = get_object_or_404(core_models.Employee, pk=employee_id)
    return render(request, 'core/view_employee.html', {
        'employee': doctor,
    })

@login_required
def create_edit_employee(request, employee_id=None):
    employee = None
    action = 'add'
    if employee_id:
        employee = get_object_or_404(core_models.Employee, pk=employee_id)
        action = 'edit' if employee else 'add'

    form = core_forms.EmployeeForm(request.POST or None, instance=employee)

    if form.is_valid():
        valid_form = form.save(commit=False)
        if action == 'add':
            valid_form.created_by = request.user
            valid_form.modified_by = request.user
        else:
            valid_form.modified_by = request.user
        valid_form.save()
        url = reverse('core_view_employee', args=(valid_form.pk,))
        return HttpResponseRedirect(url)

    return render(request, 'core/create_edit_employee.html', {
        'employee': employee,
        'form': form,
    })



def employee_registration(request):

    registrationDate = datetime.strptime('25102018', "%d%m%Y").date()
    # if datetime.now().date() != registrationDate:
    if datetime.now().date() > registrationDate:
        return render(request,'core/registrationexpiry.html')

    if request.method == 'POST':
        form = core_forms.EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            # return redirect('employee_registration_success', {
            #     'user': user
            # })
            return render(request, 'core/employee_registration_success.html', {
                    'user': user
                    })
        else:
            # if(is_email(core_models.UserProfile.email)):
            #     raise forms.ValidationError("The login details are incorrect")
            # else:
            #     raise forms.ValidationError("The email details are incorrect")
            messages.error(request, "Error")
            print("invalid form")
    else:
        form = core_forms.EmployeeRegistrationForm()
    return render(request, 'core/employee_registration.html', {
            'form': form
            })

def employee_registration_success(request):
    return render(request, 'core/employee_registration_success.html')

def register(request):
    return render(request, 'registration/register.html')
