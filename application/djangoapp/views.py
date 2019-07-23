from django.http import HttpResponse, QueryDict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apipkg import api_manager as api
from .models import *
import json


@csrf_exempt
def customer(request):
    if request.method == 'GET':
        customers = Customer.objects.all().values()
        customers_list = list(customers)  # important: convert the QuerySet to a list object
        return JsonResponse(customers_list, safe=False)
    elif request.method == 'POST':
        # convert json to dictionary
        arg = json.loads(request.POST.get("arg"))
        c = Customer(firstName=arg['firstName'], lastName=arg['lastName'], fidelityPoint=0)
        c.save()
        return HttpResponse("added")
    else:
        return HttpResponse("Bad request")

def promo(request):
    res = api.send_request('gestion-promotion', '/promo')
    return HttpResponse(res)

def add_promo(request):
    b = '{"isFlat":true, "flat":0, "percent":45, "productId":1}'
    res = api.post_request('promo', '/promo', '{"isFlat":true, "flat":0, "percent":45, "productId":1}')
    return HttpResponse(res)
