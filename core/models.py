# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):
    """
    Creates the "User Manager" for our custom user model
    """

    def create_user(self, username, first_name, last_name, password=None):
        """
        Creates new user profile
        """

        if not username:
            raise ValueError('Users must have an username.')

        # email = self.normalize_email(email)
        user = self.model(username=username, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, password):
        """
        Creates the superuser
        """

        user = self.create_user(username, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Custom "User Profile" model for online_test app
    """

    username    = models.CharField(max_length=10, unique=True)
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    mobile      = models.CharField(max_length=10)
    email       = models.EmailField(max_length=255, unique=True)
    business_unit=models.CharField(max_length=255)
    team        = models.CharField(max_length=255)
    employee_id = models.OneToOneField('Employee', unique=True, null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Used to get the full name of the user
        """

        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):

        """
        Used to ge the short name of the user
        """

        return self.first_name

    def ___str__(self):

        """
        Django uses this method when it needs to convert the object to a string
        """

        return self.username

class Employee(models.Model):
    """
    It is an employee model which employees can be stored.
    """

    employee_id     = models.CharField(max_length=10, unique=True)
    first_name      = models.CharField(max_length=255)
    last_name       = models.CharField(max_length=255)
    designation     = models.CharField(max_length=255)
    is_active       = models.BooleanField(default=True)
    # created_by      = models.ForeignKey('UserProfile', related_name='core_employee_created_by', editable=False)
    # modified_by     = models.ForeignKey('UserProfile', related_name='core_employee_modified_by', editable=False)
    created_on      = models.DateTimeField(auto_now_add=True)
    modified_on     = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        """
        Returns the full name of the employee
        """

        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        """
        Django uses this method when it needs to convert the object to string
        """

        return self.employee_id
