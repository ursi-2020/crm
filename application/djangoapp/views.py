from django.http import HttpResponse, QueryDict
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apipkg import api_manager as api
import uuid
from .forms import *
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


def customer_by_ID(request, userId):
    try:
        customer = Customer.objects.filter(id=userId).values()
    except Customer.DoesNotExist:
        return JsonResponse({"error": "user not found"})

    if customer:
        print(customer)
        customer = list(customer)  # important: convert the QuerySet to a list object
        return JsonResponse(customer, safe=False)

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


def update_db(request):
    if request.method == 'POST':
        customer = CustomerForm(request.POST, request.FILES)
        if customer.is_valid():
            data = request.FILES['file'].read()
            parsed_json = (json.loads(data))
            '''print(parsed_json)'''
            Customer.objects.all().delete()
            for client in parsed_json['clients']:
                id_1 = uuid.uuid1()
                print(id_1)
                if 'Compte' in client:
                    new_client = Customer(id1 = id_1, lastName = client['Nom'], firstName = client['Prenom'], fidelityPoint = client['Credit'], payment = client['Paiement'], account = client['Compte'])
                else:
                    new_client = Customer(id1 = id_1, lastName=client['Nom'], firstName=client['Prenom'],fidelityPoint=client['Credit'], payment=client['Paiement'])
                new_client.save()
            SomeModel_json = serializers.serialize("json", Customer.objects.all())
            data = {"Clients_json": SomeModel_json}
            return JsonResponse(data)
    else:
        client = CustomerForm()
        return render(request, 'djangoapp/update_db.html',{'form': client})