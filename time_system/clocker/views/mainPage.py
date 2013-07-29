from django.template import RequestContext, loader
from django.http import HttpResponse
from clocker.models import Employee


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
        message = "You are clock in. You clocked in at " 
    if recentShift is not None and not status:
        message = "You are clocked out. You last clocked out at "
        timeStamp = recentShift.time_out
    
    t = loader.get_template('mainPage.html')
    c = RequestContext(request, {
        'employee': employee,
        'employees': employees,
        'status': status,
        'message': message,
        'timeStamp': timeStamp
    })

    return HttpResponse(t.render(c), content_type="text/html")