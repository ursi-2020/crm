[Sommaire](https://ursi-2020.github.io/Documentation/)
# CRM-app

This application manage all data from customers.

# Home Page

The CRM home page contains following elements :
- A table of all clients registered in the data base
- Link 'Importer clients' allowing go to page for adding clients

**Service name** : `crm`

**URL** : `api`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

# JSON API

## API list:

[Show all customers](#show-all-customers)

[Show one customer by id](#show-one-customer)

[Show one customer by email](#show-one-customer-by-email)

[Add a customer by file](#add-a-customer-by-file)

[Create new customer](#create-new-customer)

[Credit customers](#credit-customers)

[Get the credit of customers](#get-the-credit-of-customers)

[Allow credit](#allow-credit)

[Get tickets](#get-tickets)



## Show all customers

Get the details of all customers registered in the CRM db

**Service name** : `crm`

**URL** : `api/data`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
[
      {
           "id": 1,
           "IdClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
           "Nom": "Jacquie",
           "Prenom": "Bloggs",
           "Credit": "420",
           "Date_paiement":	"2019-01-11",
           "Montant": 1330,
           "NbRefus": 0,
           "Compte": "BKN1CST53",
           "Age": 42,
           "Sexe": "h",
           "Email":	"Jacquie@mimi.com",
           "Phone": "0102030405"
      },
      {
           "id": 2,
           "IdClient": "2c5b24e0-0d48-11ea-b85e-08002751d198",
           "Nom": "Michelle",
           "Prenom": "Bloggs",
           "Credit": "780",
           "Date_paiement":	"2019-01-18",
           "Montant": 4569,
           "NbRefus": 1,
           "Compte": "BKN1CST83",
           "Age": 42,
           "Sexe": "f",
           "Email":	"Michelle@mimi.com",
           "Phone": "0102089405"
         }
]
```

## Show one customer

Get the details of a customer registered in the CRM db with ID.

**Service name** : `crm`

**URL** : `api/data/<slug:IdClient>`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
[
     {
       "id": 3,
       "IdClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
       "Nom": "Jacquie",
       "Prenom": "Bloggs",
       "Credit": "420",
       "Date_paiement":	"2019-01-11",
       "Montant": 1330,
       "NbRefus": 0,
       "Compte": "BKN1CST53",
       "Age": 42,
       "Sexe": "h",
       "Email":	"Jacquie@mimi.com",
       "Phone": "0102030405"
     }
 ]
```

# Show one customer by email

Get the details of a customer registered in the CRM db with its email.

**Service name** : `crm`

**URL** : `api/data/<slug:IdClient>`

**Method** : `POST`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
{
   "email": "eddison@ursi.fr"
}
```

## Add a customer by file

Register a new customer in CRM db

**Service name** : `crm`

**URL** : `/api/update_db`

**Method** : `POST`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
{"clients" : [
        {
            "Nom": "Eddison-18",
            "Prenom": "Jean",
            "Credit": 0.0,
        "Paiement": 25,
        "Date_paiement": "2019-01-18",
            "Montant": 125,
            "Compte": "BKN1CST18"
        },
        {
            "Nom": "Sarkozy-51",
            "Prenom": "Marc",
            "Credit": 0.0,
        "Paiement": 25,
        "Date_paiement": "2019-01-08",
            "Montant": 125,
            "Compte": "BKN1CST53"
        },
        {
            "Nom": "Eddison-53",
            "Prenom": "Anne",
            "Credit": 154.62542724609375,
        "Paiement": 25,
        "Date_paiement": "2020-05-19",
            "Montant": 125
        }
    ]
}
```

## Create new customer

Register a new customer in CRM and get back its new client id

**Service name** : `crm`

**URL** : `/api/create_customer`

**Method** : `POST`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**

```json
{
    "name" : "Jon",
    "last_name" : "Doe",
    "sexe" : "f",
    "age" : 23,
    "mail" : "jon.doe@mail.com",
    "phone" : "+33638614907"
}
```

**Response:**

```json
{
    "idClient": "a14e39ce-e29e-11e9-a8cb-08002751d198"
}
```

## Credit customers

Each client with a fidelity card is credeted of 0,5 * total payment

**Service name** : `crm`

**URL** : `/api/credit`

**Method** : `POST`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
{"Tickets" : [
                {
                    "carteFid": 33,
                    "Montant": 26
                },
                {
                    "carteFid": 42,
                    "Montant": 55
                }
            ]
}
```

## Get the credit of customers

Get the credit of a customer with its carteFid number

**Service name** : `crm`

**URL** : `/api/credit/<carteFid>`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
{
    "carteFid": 33,
    "Credit": 13
}
```

## Allow credit

Check if client is allowed to contact credit and schedule the credit.

**Service name** : `crm`

**URL** : `/api/allow_credit/

**Method** : `POST`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
{
    "idClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
    "Montant": 36000,
    "Date": "2019-12-06"
}
```

**Response:**
```json
{
    "idClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
    "Allowed": true
}
```

## Get tickets

Get the list of all tickets

**Service name** : `crm`

**URL** : `/api/get_tickets/

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
{"tickets":[
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
                    "prixAvant" : 800,
                    "prixApres": 400,
                    "promo": 50,
                    "quantity": 2
                  },
                  {
                    "codeProduit": "X1-9",
                    "prixAvant" : 48,
                    "prixApres": 24,
                    "promo": 50,
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
                    "prixAvant" : 36,
                    "prixApres": 18,
                    "promo": 50,
                    "quantity": 2
                  }
                ]
              }
          ]
}
```
