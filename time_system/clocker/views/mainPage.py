from django.template import RequestContext, loader
from django.http import HttpResponse
from clocker.models import Employee
from clocker.views.timesheet import getPayPeriod
from datetime import date, timedelta
from settings import DT_FORMAT, D_FORMAT

def mainPage(request):
    
    employee = request.user
    employees = [employee]
    if employee.is_superuser:
        employees = Employee.objects.filter(is_active=True)

    status = employee.isClockedIn()
    recentShift = employee.getCurrentShift()
   
    timeStamp = ''
    message = "It appears that you have never clocked in before.\
                Please clock in to start using Timeclock!"

    if recentShift is not None:
        timeStamp = recentShift.time_in
        message = "You are clocked in. You clocked in at " 
    if recentShift is not None and not status:
        message = "You are clocked out. You last clocked out at "
        timeStamp = recentShift.time_out

    today = date.today()
    start_week = today - timedelta(today.weekday())
    end_week = start_week + timedelta(7)   
    periodData = getPayPeriod(start_week.strftime(D_FORMAT), end_week.strftime(D_FORMAT), employee.username)

    t = loader.get_template('mainPage.html')
    c = RequestContext(request, {
        'employee': employee,
        'employees': employees,
        'status': status,
        'message': message,
        'timeStamp': timeStamp,
        'start_week': date.strftime(start_week, D_FORMAT),
        'today': date.strftime(today, D_FORMAT),
        'weekly_regular': periodData['pay_period']['period_regular'],
        'weekly_overtime': periodData['pay_period']['period_overtime']
    })

    return HttpResponse(t.render(c), content_type="text/html")
