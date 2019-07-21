from django.http import HttpResponse
from django.http import JsonResponse
from apipkg import api_manager as api
from .models import *


def customer(request):
    if request.method == 'GET':
        customers = Customer.objects.all().values()
        customers_list = list(customers)  # important: convert the QuerySet to a list object
        return JsonResponse(customers_list, safe=False)
    elif request.method == 'POST':
        
        return HttpResponse("added")
    else:
        return HttpResponse("Bad request")

