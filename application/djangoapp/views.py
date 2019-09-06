from django.http import HttpResponse, QueryDict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apipkg import api_manager as api
from .models import *
import json

def index(request):
    return render(request, 'djangoapp/index.html')

@csrf_exempt
def customer(request):
    if request.method == 'GET':
        customers = Customer.objects.all().values()
        customers_list = list(customers)  # important: convert the QuerySet to a list object
        return JsonResponse(customers_list, safe=False)
    elif request.method == 'POST':
        # convert json to dictionary

        body_unicode = request.body.decode('utf-8')
        arg = json.loads(body_unicode)
        c = Customer(firstName=arg['firstName'], lastName=arg['lastName'], fidelityPoint=0)
        c.save()
        return HttpResponse("added")
    else:
        return HttpResponse("Bad request")

def promo(request):
    res = api.send_request('gestion-promotion', 'api/v1/promo')
    return HttpResponse(res)

def add_promo(request):
    b = {"isFlat":True, "flat":0, "percent":45, "productId":1}
    res = api.post_request('gestion-promotion', 'api/v1/promo', body=b)
    return HttpResponse(res)

def test(request):
    j = '{"firstName":"Quentin", "lastName":"Reynaud"}'
    api.post_request('crm', 'customer/', j)
    return HttpResponse("created")
