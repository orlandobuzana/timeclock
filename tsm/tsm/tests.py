"""
" tsm/tests.py
" Contributing Authors:
"    Bretton Murphy (Visgence, Inc)
"
" (c) 2012 Visgence, Inc.
"""

# System Imports
from django.test import TestCase
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
from datetime import timedelta

# Local Imports
from tsm.models import Employee, Shift



''''''''''''''''''''''''''''''''''''
'''         Model Tests          '''
''''''''''''''''''''''''''''''''''''


class ShiftManagerTests(TestCase):
    fixtures = ['test_employees.json']

    def test_clockedIn_clockedIn(self):
        ''' A clocked in Employee should get back True '''
        
        emp = Employee.objects.get(username="HourlyUser")
        shift = Shift(employee=emp, shift_start=timezone.now())
        shift.save()

        self.assertTrue(Shift.objects.clocked_in(emp))

    def test_clockedIn_clockedOut(self):
        ''' A clocked out Employee should get back False '''

        emp = Employee.objects.get(username="HourlyUser")

        now = timezone.now()
        shift = Shift(employee=emp, shift_start=now, shift_end=now+timedelta(hours=1))
        shift.save()

        self.assertFalse(Shift.objects.clocked_in(emp))

    def test_clockedIn_badUser(self):
        ''' A non Employee object should raise a TypeError '''

        emp = {"user": "fake"}
        self.assertRaises(TypeError, Shift.objects.clocked_in, emp)
    
    def test_clockedIn_multipleClockedIn(self):
        ''' MultipleObjectsReturned should raise on multiple clocked in shifts found.'''

        emp = Employee.objects.get(username="HourlyUser")
        shift = Shift(employee=emp, shift_start=timezone.now())
        shift2 = Shift(employee=emp, shift_start=timezone.now())
        shift.save()
        shift2.save()

        self.assertRaises(MultipleObjectsReturned, Shift.objects.clocked_in, emp)








