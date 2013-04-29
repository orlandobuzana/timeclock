"""
" tsm/models.py
" Contributing Authors:
"    Bretton Murphy (Visgence, Inc)
"
" (c) 2012 Visgence, Inc.
"""

# System Impots
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Project(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True) 


class Employee(AbstractBaseUser):
    permissions = (
        ('EM', 'Employee'),
        ('MG', 'Manager'),
        ('OW', 'Owner')
    )

    username = models.CharField(max_length=15, unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    hourly_rate = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=6)
    salary = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9)
    salaried = models.BooleanField(default=False)
    projects = models.ManyToManyField(Project)
    premission = models.CharField(choices=permissions, default="EM", max_length=2)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Shift(models.Model):

    shift_start = models.IntegerField()
    shift_end = models.IntegerField(null=True, blank=True)
    emploee = models.ForeignKey(Employee)
    project = models.ForeignKey(Project, blank=True, null=True)
    miles = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=6)


