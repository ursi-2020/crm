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
    Customer(firstName="Sarah", lastName="Belmok").save()
    return HttpResponse("New user created")
