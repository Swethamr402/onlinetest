"""online_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views as core_views

urlpatterns = [
    url(r'^register/$', core_views.register, name='auth_register'),
    url(r'home/$', core_views.home, name='core_home'),
    url(r'dashboard/$', core_views.dashboard, name='core_dashboard'),

    url(r'^employee/register/$',
        core_views.employee_registration,
        name='employee_registration'),

    url(r'^employee/success_register/$',
        core_views.employee_registration_success,
        name='employee_registration_success'),

    url(r'^employees/$',
        core_views.list_employees,
        name='core_list_employees'),

    url(r'^employee/create/$',
        core_views.create_edit_employee,
        name='core_create_employee'),

    url(r'^employee/(?P<employee_id>\d+)/$',
        core_views.view_employee,
        name='core_view_employee'),

    url(r'^employee/(?P<employee_id>\d+)/edit/$',
        core_views.create_edit_employee,
        name='core_edit_employee'),

    # url(r'^employee/(?P<employee_id>\d+)/delete/$',
    #     core_views.DeleteEmployeeView.as_view(),
    #     name='core_delete_employee'),
]
