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
        shift = Shift(employee=emp, shift_start=1367591417)
        shift.save()

        self.assertTrue(Shift.objects.clocked_in(emp))

    def test_clockedIn_clockedOut(self):
        ''' A clocked out Employee should get back False '''

        emp = Employee.objects.get(username="HourlyUser")
        shift = Shift(employee=emp, shift_start=1367591417, shift_end=1367691417)
        shift.save()

        self.assertFalse(Shift.objects.clocked_in(emp))

    def test_clockedIn_badUser(self):
        ''' A non Employee object should raise a TypeError '''

        emp = {"user": "fake"}
        self.assertRaises(TypeError, Shift.objects.clocked_in, emp)
    
    def test_clockedIn_multipleClockedIn(self):
        ''' MultipleObjectsReturned should raise on multiple clocked in shifts found.'''

        emp = Employee.objects.get(username="HourlyUser")
        shift = Shift(employee=emp, shift_start=1367591417)
        shift2 = Shift(employee=emp, shift_start=1467591417)
        shift.save()
        shift2.save()

        self.assertRaises(MultipleObjectsReturned, Shift.objects.clocked_in, emp)








