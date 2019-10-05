[Sommaire](https://ursi-2020.github.io/Documentation/)
# CRM-app

This application manage all data from customers.

It includes:
 - uuid
 - Last name
 - First name
 - Credit
 - Payment
 - account

# Home Page

The CRM home page contains following elements :
- A table of all clients registered in the data base
- Link 'Importer clients' alowing go to page for adding clients

**Service name** : `crm`

**URL** : `api`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

# JSON API

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
    "IdClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
    "Nom": "Jacquie",
    "Prenom": "Bloggs",
    "Credit": "42,00",
    "Paiement": 0,
    "Compte": "BKN1CST53"
  },
  {
    "IdClient": "a14f4a08-e29e-11e9-a8cb-08002751d198",
    "Nom": "Michelle",
    "Prenom": "Bigoudi",
    "Credit": "69,00",
    "Paiement": 3,
    "Compte": ""
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
       "idClient": "a14e39ce-e29e-11e9-a8cb-08002751d198",
       "Nom": "Jacquie",
       "Prenom": "Bloggs",
       "Credit": "42.00",
       "Paiement": 0,
       "Compte": "BKN1CST53"
     }
 ]
```


## Add a customer

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
                    "Paiement": 0,
                    "Compte": "BKN1CST18"
                },
                {
                    "Nom": "Sarkozy-51",
                    "Prenom": "Marc",
                    "Credit": 0.0,
                    "Paiement": 0
                },
                {
                    "Nom": "Eddison-53",
                    "Prenom": "Anne",
                    "Credit": 154.62542724609375,
                    "Paiement": 3,
                    "Compte": "BKN1CST53"
                }
            ]
}
```
