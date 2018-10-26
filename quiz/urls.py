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

from . import views as quiz_views

urlpatterns = [

    url(r'^questions/$',
        quiz_views.list_questions,
        name='quiz_list_questions'),

    url(r'^home/$',
        quiz_views.home,
        name='quiz_home'),

        url(r'^dashboard/$',
    # url(r'^toppersresults(?P<quiz_id>\d+)/$',
        quiz_views.view_toppers_results,
        name='dashboard'),

    url(r'^startquiz/(?P<quiz_id>\d+)/$',
        quiz_views.start_quiz,
        name='start_quiz'),

    url(r'^quizlive/(?P<quiz_id>\d+)/$',
        quiz_views.quiz_live,
        name='quiz_live'),

    url(r'^quizlive/finishquiz(?P<quiz_id>\d+)/$',
        quiz_views.quiz_live,
        name='finishquiz'),

    url(r'^individualresult/(?P<header_id>\d+)/$',
        quiz_views.view_individual_results,
        name='individual_result'),


    url(r'^toppersresults(?P<quiz_id>\d+)/$',
        quiz_views.view_toppers_results,
        name='toppers_results'),

    # url(r'^employee/create/$',
    #     core_views.create_edit_employee,
    #     name='core_create_employee'),
    #
    # url(r'^employee/(?P<employee_id>\d+)/$',
    #     core_views.view_employee,
    #     name='core_view_employee'),
    #
    # url(r'^employee/(?P<employee_id>\d+)/edit/$',
    #     core_views.create_edit_employee,
    #     name='core_edit_employee'),

    # url(r'^employee/(?P<employee_id>\d+)/delete/$',
    #     core_views.DeleteEmployeeView.as_view(),
    #     name='core_delete_employee'),
]
