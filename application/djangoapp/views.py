from django.http import HttpResponse, QueryDict
from django.http import JsonResponse
from django.core import serializers
from decimal import Decimal
from datetime import datetime, timedelta, date
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
    customer = Customer.objects.filter(IdClient=userId).values()
    if not customer.exists():
        return JsonResponse({"error": "user not found"})

    else:
        customer = list(customer)  # important: convert the QuerySet to a list object
        return JsonResponse(customer, safe=False)

def getCredit(request, idClient):
    customer = Customer.objects.filter(IdClient=idClient).values()
    if not customer.exists():
        return JsonResponse({"error": "Customer not found"})

    else:
        customer = list(customer)
        result = {"idClient": customer[0]["IdClient"], "Credit": customer[0]["Credit"]}
        return JsonResponse(result, safe=False)

def promo(request):
    res = api.send_request('gestion-promotion', 'api/v1/promo')
    return HttpResponse(res)

def add_promo(request):
    b = {"isFlat":True, "flat":0, "percent":45, "productId":1}
    res = api.post_request('gestion-promotion', 'api/v1/promo', body=b)
    return HttpResponse(res)

def test(request):
    body = {
        "idClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
        "Montant": 36000,
        "Date": "2019-12-06"
    }
    api.post_request2('gestion-paiement', 'api/proceed-payement', body)
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
                if 'Compte' in client:
                    new_client = Customer(IdClient = idClient, Nom = client['Nom'], Prenom = client['Prenom'], Credit = client['Credit'], Date_paiement = client['Date_paiement'], Montant = client['Montant'], Compte = client['Compte'])
                else:
                    new_client = Customer(IdClient=idClient, Nom=client['Nom'], Prenom=client['Prenom'],
                                          Credit=client['Credit'], Date_paiement = client['Date_paiement'], Montant = client['Montant'])

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
    tickets = (json.loads(res))
    return update_save_tickets(tickets)

# obsolete use function in apps.py
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
# obsolete use function in apps.py
def schedule_task(body):
    headers = {'Host': 'scheduler'}
    r = requests.post(api.api_services_url + 'schedule/add', headers=headers, json=body)
    print("schedule error code: ")
    print(r.status_code)
    print(r.text)
    return
'''==========================================E-COMMERCE============================================'''
@csrf_exempt
def create_customer(request):
    idClient = uuid.uuid1()
    for key in dict(request.POST.lists()) :
        client = json.loads(key)
    new_client = Customer(IdClient= idClient, Nom=client['last_name'], Prenom=client['name'], Sexe=client['sexe'], Age=client['age'], Email=client['mail'], Phone=client['phone'])

    new_client.save()
    return JsonResponse({"idClient": uuid.uuid1()})

def update_save_tickets(tickets):
    error = False
    for t in tickets:
        if t['client'] != '':
            try:
                customer = Customer.objects.get(IdClient=t['client'])
                customer.Credit = customer.Credit + int(t['prix']) / 2
                customer.save()

                # Save the ticket
                new_ticket = Ticket(DateTicket=t['date'], Prix=t['prix'], Client=t['client'],
                                    PointsFidelite=t['pointsFidelite'], ModePaiement=t['modePaiement'])
                new_ticket.save()
                if t['articles'] != '':
                    for article in t['articles']:
                        new_article = PurchasedArticle(CodeProduit=article['CodeProduit'],
                                                       PrixAvant=article['PrixAvant'], PrixApres=article['PrixApres'],
                                                       Promo=article['Promo'], Quantity=article['Quantity'],
                                                       ticket=new_ticket)
                        new_article.save()

            except ObjectDoesNotExist:
                error = True
    if error:
        return JsonResponse({"Error": "Client does not exist"})
    return JsonResponse({"SUCESS": "Fidelity point updated"})


@csrf_exempt
def credit_ecommerce(request):
    res = api.send_request('e-commerce', 'getTickets')
    tickets = json.loads(res)
    return update_save_tickets(tickets)

def schedule_credit_ecommerce(request):
    clock_time = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
    time = time + timedelta(seconds=180)
    time_str = time.strftime('%d/%m/%Y-%H:%M:%S')
    body = {
        "target_app": 'crm',
        "target_url": 'api/credit_ecommerce',
        "time": time_str,
        "recurrence": "day",
        "data": '{}',
        "source_app": "crm",
        "name": "CRM-credit-clients-ecommerce"
    }
    schedule_task(body)
    return redirect('index')

'''=======================================END E-COMMERCE==========================================='''

@csrf_exempt
def allow_credit(request):
   # return JsonResponse({"idClient": "a14e39ce-e29e-11e9-a8cb-08002751d198", "Allowed": True})
    # Get client id, check if client is allowed, get credit amount, schedule a task

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        arg = json.loads(body_unicode)
        try:
            c = Customer.objects.get(IdClient=arg['idClient'])
            if (arg['Date'] and arg['Montant']):
                if c.NbRefus < 1:
                    c.Date_paiement = arg['Date']
                    c.Montant = arg['Montant']
                    c.save()
                    return JsonResponse({"idClient": arg['idClient'], "Allowed": True})
                else:
                    return JsonResponse({"idClient": arg['idClient'], "Allowed": False})
            else:
                return JsonResponse({"Error": 'Missing fields', "Allowed": False})
        except Customer.DoesNotExist:
            return JsonResponse({"Error": 'Client does not exist', "Allowed": False})


@csrf_exempt
def paiement(request):
    #Select all paiement according to the date
    #today = date.today()
    today = api.send_request('scheduler', 'clock/time')
    time = datetime.strptime(today, '"%d/%m/%Y-%H:%M:%S"')
    #Get all customer that have to pay this day
    c = Customer.objects.filter(Date_paiement=time)

    body = {}
    for client in c:
        body["client_id"] = client.IdClient
        body["card"] = client.Compte
        body["amount"] = client.Montant
        paiement = api.post_request2('gestion-paiement', 'api/proceed-payement', body)
        success = json.loads(paiement[1].content)["status"]
        #if error set it in crm
        if success == "OK":
            client.Montant = 0
        else:
            client.NbRefus = client.NbRefus + 1
            client.Date_paiement = client.Date_paiement + timedelta(days=1)

        client.save()
    return JsonResponse({"State": "finished"})


def get_tickets(request):
    return JsonResponse({"tickets":[
                          {
                            "id": 42,
                            "date": "2019-10-09T17:01:29.408701Z",
                            "prix": 424,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 0,
                            "modePaiement": "CASH",
                            "articles": [
                              {
                                "codeProduit": "X1-0",
                                "quantity": 2
                              },
                              {
                                "codeProduit": "X1-9",
                                "quantity": 1
                              }
                            ]
                          },
                          {
                            "id": 38,
                            "date": "2019-10-09T18:03:45.408701Z",
                            "prix": 7582,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 18,
                            "modePaiement": "CARD",
                            "articles": [
                              {
                                "codeProduit": "X1-4",
                                "quantity": 2
                              }
                            ]
                          }
                        ]})
