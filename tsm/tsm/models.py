"""
" tsm/models.py
" Contributing Authors:
"    Bretton Murphy (Visgence, Inc)
"
" (c) 2012 Visgence, Inc.
"""

# System Impots
from django.contrib.auth.models import AbstractBaseUser, AbstractBaseManager
from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from decimal import Decimal


class ProjectManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = ProjectManager()

    def __unicode__(self):
        return self.name


class User(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True, db_index=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField()

    USERNAME_FIELD = "username"


class EmployeeManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class Employee(User):
    hourly_rate = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=6)
    salary = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9)
    salaried = models.BooleanField(default=False)
    projects = models.ManyToManyField(Project)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def _clocked_in(self):
        return Shift.objects.clocked_in(self)

    def _projects(self):
        return self.projects.filter(is_active=True)

    clocked_in = property(_clocked_in)
    active_projects = property(_projects)


class ShiftManager(models.Manager):
    def clocked_in(self, employee):
        '''
            Checks if an Employee is clocked in or not.

            Keyword Arguments:
                employee - Employee to check clocked in status.

            Return: True if clocked in and False otherwise.
        '''

        if not isinstance(employee, Employee):
            raise TypeError("%s is not an object of the type Employee"%str(employee))
        
        try:
            self.get(shift_end=None, employee=employee)
            return True
        except Shift.DoesNotExist:
            return False
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned("%s has multiple shifts that are clocked in!"%str(employee))

        return False


class Shift(models.Model):
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField(null=True, blank=True)
    hours = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=4)
    employee = models.ForeignKey(Employee)
    
    objects = ShiftManager()

    def save(self, *args, **kwargs):
        if self.shift_end is None:
            self.hours = 0.0
        elif self.shift_start is not None and self.shift_end is not None:
            diff = self.shift_end - self.shift_start
            self.hours = Decimal(diff/3600.0).quantize(Decimal('1.00'))

        super(Shift, self).save(*args, **kwargs)


class ShiftSummary(models.Model):
    shift = models.ForeignKey(Shift)
    miles = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=6)
    notes = models.TextField(blank=True)
    project = models.ForeignKey(Project)
    hours = models.DecimalField(decimal_places=2, max_digits=4)


