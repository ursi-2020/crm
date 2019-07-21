from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from apipkg import api_manager as api
from .models import *
import json

def getCustomerInfo(request):
    customers = Customer.objects.all().values()
    customers_list = list(customers)  # important: convert the QuerySet to a list object
    return JsonResponse(customers_list, safe=False)


def creatCustomer(request):
    Customer(firstName="Sarah", lastName="Belmok", fidelityPoint=42).save()
    print("new user created")
    return HttpResponse("New user created")

def createCustomerPost(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)  # request.raw_post_data w/ Django < 1.4
        try:
            data = json_data['data']
        except KeyError:
            HttpResponseServerError("Malformed data!")
        HttpResponse("Got json data")