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
from django.utils.dateparse import parse_datetime

def index(request):
    customers = Customer.objects.all().values()
    customers = list(customers)
    for c in customers:
        c['Credit'] = round((c['Credit'] / 100), 2)
    return render(request, 'djangoapp/index.html', locals())
"""
Get all info about customers
"""
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

"""
Get one customer with its clientId
"""
def customer_by_ID(request, userId):
    customer = Customer.objects.filter(IdClient=userId).values()
    if not customer.exists():
        return JsonResponse({"error": "user not found"})

    else:
        customer = list(customer)  # important: convert the QuerySet to a list object
        return JsonResponse(customer, safe=False)

'''
    Get client information with his email
    Send email with post request {email: test@tst.com}
'''
@csrf_exempt
def customer_by_email(request):
    body_unicode = request.body.decode('utf-8')
    arg = json.loads(body_unicode)
    try:
        c = Customer.objects.filter(Email=arg['email']).values()
        c = list(c)
        if len(c) > 0:
            return JsonResponse(c[0], safe=False)
        else:
            return JsonResponse({"Error": 'Client does not exist'})

    except Customer.DoesNotExist:
        return JsonResponse({"Error": 'Client does not exist'})


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
        "email": "eddison@ursi.fr"
    }
    api.post_request2('crm', 'api/data/email', json.dumps(body))
    return HttpResponse("sended")


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
                    new_client = Customer(IdClient = idClient, Nom = client['Nom'], Prenom = client['Prenom'], Credit = client['Credit'], Date_paiement = client['Date_paiement'], Montant = client['Montant'], Compte = client['Compte'], Email = client['Email'])
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

"""
This function is called by the scheduler
to gets all tickets from gestion-magasin
then add credit to customers
and save tickets in the DB
"""
@csrf_exempt
def credit(request):
    res = api.send_request('gestion-magasin', 'api/sales')
    tickets = (json.loads(res))
    return update_save_tickets(tickets, 'magasin')


'''==========================================E-COMMERCE============================================'''
@csrf_exempt
def create_customer(request):
    idClient = uuid.uuid1()
    return create_customer_with_id(request, idClient)

@csrf_exempt
def create_customer_with_id(request, id):
    body_unicode = request.body.decode('utf-8')
    client = json.loads(body_unicode)
    new_client = Customer(IdClient=id, Nom=client['Nom'], Prenom=client['Prenom'], Email=client['email'],
                          Credit=client['Credit'], Montant=client['Paiement'], Compte=client['Compte'])

    new_client.save()
    return JsonResponse({"idClient": id})

@csrf_exempt
def create_customer_with_id_test(request):
    return create_customer_with_id(request, 'a14e39ce-e29e-11e9-a8cb-08002751d198')

"""
This function is called by the scheduler
to gets all tickets from e-commerce
then add credit to customers
and save tickets in the DB
"""
@csrf_exempt
def credit_ecommerce(request):
    res = api.send_request('e-commerce', 'ecommerce/getTickets')
    tickets = json.loads(res)
    return update_save_tickets(tickets, 'e-commerce')

"""
Add credit to customers
and save tickets in the DB
Add the source of the ticket -> TODO
"""
def update_save_tickets(tickets, src):
    error = False
    for t in tickets['tickets']:
        if t['client'] != '':
            try:
                # Update customer fidelity points
                if src == 'e-commerce':
                    customer = Customer.objects.get(Email=t['client'])
                else:
                    customer = Customer.objects.get(IdClient=t['client'])
                customer.Credit = customer.Credit + int(t['prix']) / 2
                customer.save()

                # Save the ticket
                new_ticket = Ticket(DateTicket=parse_datetime(t['date']), Prix=t['prix'], Client=t['client'],
                                    PointsFidelite=t['pointsFidelite'], ModePaiement=t['modePaiement'])
                new_ticket.save()
                if t['articles'] != '':
                    for article in t['articles']:
                        new_article = PurchasedArticle(codeProduit=article['codeProduit'],
                                                       prixAvant=article['prix'], prixApres=article['prixApres'],
                                                       promo=article['promo'], quantity=article['quantity'],
                                                       ticket=new_ticket)
                        new_article.save()
                print('TICKET REGISTERED !')
            except ObjectDoesNotExist:
                error = True
        else :
            # Save the ticket
            new_ticket = Ticket(DateTicket=parse_datetime(t['date']), Prix=t['prix'], Client=t['client'],
                                PointsFidelite=t['pointsFidelite'], ModePaiement=t['modePaiement'])
            new_ticket.save()
            if t['articles'] != '':
                for article in t['articles']:
                    new_article = PurchasedArticle(codeProduit=article['codeProduit'],
                                                   prixAvant=article['prix'], prixApres=article['prixApres'],
                                                   promo=article['promo'], quantity=article['quantity'],
                                                   ticket=new_ticket)
                    new_article.save()
    if error:
        return JsonResponse({"Error": "Client does not exist"})
    return JsonResponse({"SUCESS": "Fidelity point updated"})

@csrf_exempt
def test_tickets(request):
    for key in dict(request.POST.lists()) :
        tickets = json.loads(key)
    error = False
    for t in tickets['tickets']:
        if t['client'] != '':
            try:
                # Save the ticket
                new_ticket = Ticket(DateTicket=parse_datetime(t['date']), Prix=t['prix'], Client=t['client'],
                                    PointsFidelite=t['pointsFidelite'], ModePaiement=t['modePaiement'])
                new_ticket.save()
                if t['articles'] != '':
                    for article in t['articles']:
                        new_article = PurchasedArticle(codeProduit=article['codeProduit'],
                                                       prixAvant=article['prix'], prixApres=article['prixApres'],
                                                       promo=article['promo'], quantity=article['quantity'],
                                                       ticket=new_ticket)
                        new_article.save()

            except ObjectDoesNotExist:
                error = True
    if error:
        return JsonResponse({"Error": "Client does not exist"})
    return JsonResponse({"SUCESS": "Fidelity point updated"})

@csrf_exempt
def generate_tickets(request):

    date_tickets = "2019-01-02T17:01:29.408701Z"
    tickets = {"tickets":[
                          {
                            "id": 44,
                            "date": date_tickets,
                            "prix": 424,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 0,
                            "modePaiement": "CASH",
                            "articles": [
                              {
                                "codeProduit": "X1-1",
                                "prix": 800,
                                "prixApres": 400,
                                "promo": 50,
                                "quantity": 2
                              },
                              {
                                "codeProduit": "X1-2",
                                "prix": 48,
                                "prixApres": 24,
                                "promo": 50,
                                "quantity": 1
                              },
                                {
                                    "codeProduit": "X1-3",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-4",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-5",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                }
                            ]
                          },
                        {
                            "id": 43,
                            "date": date_tickets,
                            "prix": 424,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 0,
                            "modePaiement": "CASH",
                            "articles": [
                                {
                                    "codeProduit": "X1-1",
                                    "prix": 800,
                                    "prixApres": 400,
                                    "promo": 50,
                                    "quantity": 2
                                },
                                {
                                    "codeProduit": "X1-2",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-3",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-4",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-5",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                }
                            ]
                        },
                        {
                            "id": 43,
                            "date": date_tickets,
                            "prix": 424,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 0,
                            "modePaiement": "CASH",
                            "articles": [
                                {
                                    "codeProduit": "X1-1",
                                    "prix": 800,
                                    "prixApres": 400,
                                    "promo": 50,
                                    "quantity": 2
                                },
                                {
                                    "codeProduit": "X1-2",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-3",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-4",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-5",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                }
                            ]
                        },
                        {
                            "id": 42,
                            "date": date_tickets,
                            "prix": 424,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 0,
                            "modePaiement": "CASH",
                            "articles": [
                                {
                                    "codeProduit": "X1-1",
                                    "prix": 800,
                                    "prixApres": 400,
                                    "promo": 50,
                                    "quantity": 2
                                },
                                {
                                    "codeProduit": "X1-2",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-3",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-4",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                },
                                {
                                    "codeProduit": "X1-5",
                                    "prix": 48,
                                    "prixApres": 24,
                                    "promo": 50,
                                    "quantity": 1
                                }
                            ]
                        },
                          {
                            "id": 38,
                            "date": date_tickets,
                            "prix": 7582,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 18,
                            "modePaiement": "CARD",
                            "articles": [
                              {
                                "codeProduit": "X1-6",
                                "prix": 36,
                                "prixApres": 18,
                                "promo": 50,
                                "quantity": 2
                              },
                                {
                                    "codeProduit": "X1-7",
                                    "prix": 36,
                                    "prixApres": 18,
                                    "promo": 50,
                                    "quantity": 2
                                },
                                {
                                    "codeProduit": "X1-8",
                                    "prix": 36,
                                    "prixApres": 36,
                                    "promo": 0,
                                    "quantity": 2
                                },
                                {
                                    "codeProduit": "X1-9",
                                    "prix": 36,
                                    "prixApres": 36,
                                    "promo": 0,
                                    "quantity": 2
                                },
                                {
                                    "codeProduit": "X1-10",
                                    "prix": 36,
                                    "prixApres": 36,
                                    "promo": 0,
                                    "quantity": 2
                                }
                            ]
                          }
                        ]}
    tickets_json = json.dumps(tickets)
    return update_save_tickets(json.loads(tickets_json))

'''=======================================END E-COMMERCE==========================================='''

"""
This function is called by gestion-paiement
It save a request of differed payment 
Each request is allowed if nbRefus is less than 1
"""
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

"""
This function is called bu the scheduler to process all differed payment each day
If payment refused the payment is differed next day
"""
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
    tickets = list(Ticket.objects.all().values())
    print(tickets)
    ticket_array = []
    for each_ticket in tickets :
        ticket = {}
        ticket['id'] = each_ticket['id']
        ticket['date'] = each_ticket['DateTicket']
        ticket['prix'] = each_ticket['Prix']
        ticket['client'] = each_ticket['Client']
        ticket['pointsFidelite'] = each_ticket['PointsFidelite']
        ticket['modePaiement'] = each_ticket['ModePaiement']
        ticket['articles'] = list(PurchasedArticle.objects.filter(ticket=each_ticket['id']).values())
        ticket_array.append(ticket)

    response_data = {'tickets' : ticket_array}

    return JsonResponse(response_data, content_type="application/json")


'''
    tickets = Ticket.objects.prefetch_related('purchased_articles').all().values()
    tickets_list = list(tickets)  # important: convert the QuerySet to a list object
    return JsonResponse({"tickets": tickets_list}, safe=False)
    
    return JsonResponse({"tickets":[
                          {
                            "id": 42,
                            "date": "2019-10-09",
                            "prix": 424,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 0,
                            "modePaiement": "CASH",
                            "articles": [
                              {
                                "codeProduit": "X1-0",
                                "prixAvant": 800,
                                "prixApres": 400,
                                "promo": 50,
                                "quantity": 2
                              },
                              {
                                "codeProduit": "X1-9",
                                "prixAvant": 48,
                                "prixApres": 24,
                                "promo": 50,
                                "quantity": 1
                              }
                            ]
                          },
                          {
                            "id": 38,
                            "date": "2019-10-09",
                            "prix": 7582,
                            "client": "a14e39ce-e29e-11e9-a8cb-08002751d198",
                            "pointsFidelite": 18,
                            "modePaiement": "CARD",
                            "articles": [
                              {
                                "codeProduit": "X1-4",
                                "prixAvant": 36,
                                "prixApres": 18,
                                "promo": 50,
                                "quantity": 2
                              }
                            ]
                          }
                        ]})
'''
