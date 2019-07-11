from django.http import HttpResponse
from django.http import JsonResponse
from apipkg import api_manager as api
from .models import *

def getCustomerInfo(request):
    customers = Customer.objects.all().values()
    customers_list = list(customers)  # important: convert the QuerySet to a list object
    return JsonResponse(customers_list, safe=False)


def creatCustomer(request):
    Customer(firstName="Sarah", lastName="Belmok", fidelityPoint=42).save()
    print("new user created")
    return HttpResponse("New user created")