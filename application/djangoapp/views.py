from django.http import HttpResponse, QueryDict
from django.http import JsonResponse
from django.core import serializers
from decimal import Decimal
from datetime import datetime, timedelta
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apipkg import api_manager as api
import uuid
from .forms import *
from .models import *
import json

def index(request):
    customers = Customer.objects.all().values()
    customers = list(customers)
    for c in customers:
        c['Credit'] = round((c['Credit'] / 100), 2)
    return render(request, 'djangoapp/index.html', locals())

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
    customer = Customer.objects.filter(carteFid=userId).values()
    if not customer.exists():
        return JsonResponse({"error": "user not found"})

    else:
        customer = list(customer)  # important: convert the QuerySet to a list object
        return JsonResponse(customer, safe=False)

def getCredit(request, carteFid):
    customer = Customer.objects.filter(carteFid=carteFid).values()
    if not customer.exists():
        return JsonResponse({"error": "Customer not found"})

    else:
        customer = list(customer)
        result = {"carteFid": customer[0]["carteFid"], "Credit": customer[0]["Credit"]}
        return JsonResponse(result, safe=False)

def promo(request):
    res = api.send_request('gestion-promotion', 'api/v1/promo')
    return HttpResponse(res)

def add_promo(request):
    b = {"isFlat":True, "flat":0, "percent":45, "productId":1}
    res = api.post_request('gestion-promotion', 'api/v1/promo', body=b)
    return HttpResponse(res)

def test(request):
    j = json.loads('{"Tickets" : [{"carteFid": 33, "Montant": 26},{"carteFid": 42,"Montant": 55}]}')
    api.post_request('crm', '/api/credit/', j)
    return HttpResponse("Credited")


def update_db(request):
    if request.method == 'POST':
        customer = CustomerForm(request.POST, request.FILES)
        if customer.is_valid():
            data = request.FILES['file'].read()
            parsed_json = (json.loads(data))
            Customer.objects.all().delete()
            for client in parsed_json['clients']:
                idClient = uuid.uuid1()
                if ('Compte' in client and 'carteFid' in client):
                    new_client = Customer(IdClient = idClient, Nom = client['Nom'], Prenom = client['Prenom'], Credit = client['Credit'], Paiement = client['Paiement'], Compte = client['Compte'], carteFid = client['carteFid'])
                elif ('carteFid' in client and not 'Compte' in client):
                    new_client = Customer(IdClient = idClient, Nom=client['Nom'], Prenom=client['Prenom'],Credit=client['Credit'], Paiement=client['Paiement'], carteFid = client['carteFid'])
                elif ('Compte' in client and not 'carteFid' in client):
                    new_client = Customer(IdClient=idClient, Nom=client['Nom'], Prenom=client['Prenom'],
                                          Credit=client['Credit'], Paiement=client['Paiement'], Compte=client['Compte'])
                else:
                    new_client = Customer(IdClient=idClient, Nom=client['Nom'], Prenom=client['Prenom'],
                                          Credit=client['Credit'], Paiement=client['Paiement'])

                new_client.save()
            SomeModel_json = serializers.serialize("json", Customer.objects.all())
            data = {"Clients_json": SomeModel_json}
            return redirect('index')
    else:
        client = CustomerForm()
        return render(request, 'djangoapp/update_db.html',{'form': client})

@csrf_exempt
def credit(request):
    res = api.send_request('gestion-magasin', 'api/sales')
    tickets = json.loads(res)
    error = False
    for t in tickets:
        if t['client'] != '':
            try:
                customer = Customer.objects.get(carteFid=t['client'])
                customer.Credit = customer.Credit + int(t['prix']) / 2
                customer.save()

            except ObjectDoesNotExist:
                error = True
    if error:
        return JsonResponse({"Error": "Client does not exist"})
    return JsonResponse({"SUCESS": "Fidelity point updated"})


def schedule_credit(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=180)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    body = {
        "target_app": 'crm',
        "target_url": 'api/credit',
        "time": time_str,
        "recurrence": "day",
        "data": '{}',
        "source_app": "crm",
        "name": "CRM-credit-clients"
    }
    schedule_task(body)
    return redirect('index')

def schedule_task(body):
    headers = {'Host': 'scheduler'}
    r = requests.post(api.api_services_url + 'schedule/add', headers=headers, json=body)
    print("schedule error code: ")
    print(r.status_code)
    print(r.text)
    return

@csrf_exempt
def create_customer(request) :
    idClient = uuid.uuid1()

    return JsonResponse({"carteFid": uuid.uuid1()})

