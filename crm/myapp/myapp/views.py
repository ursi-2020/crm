from django.http import HttpResponse
from django.http import JsonResponse
from apipkg import api_manager as api
from .models import *


def index(request):
    time = api.send_request('scheduler', 'clock/time')
    return HttpResponse("L'heure de la clock est %r" % time)


def getCustomerInfo(request):
    customers = Customer.objects.all().values()
    customers_list = list(customers)  # important: convert the QuerySet to a list object
    return JsonResponse(customers_list, safe=False)


def creatCustomer(request):
    res = api.send_request('test_app', '/create_customer')
    return HttpResponse(res)


def testApp(request):
    res = api.send_request('test_app', '/customers')
    return HttpResponse(res)

def addToScheduler(request):
    res = api.post_request('scheduler', '/schedule/add', '{"target_url"="/create_customer", "target_app"="test_app", "time"="3", "recurrence"="1", "data"=""}')
    return HttpResponse(res)
