# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name','email', 'mobile')

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Employee)
