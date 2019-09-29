# CRM-app

This application manage all data from customers.

It includes:
 - firstName
 - lastName
 - fidelityPoint
 - payment
 - account

# JSON API

## Show all customers

Get the details of all customers registered in the CRM db

**Service name** : `crm`

**URL** : `/api/data`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
[
  {
    "id": 1,
    "firstName": "Jacquie",
    "lastName": "Bloggs",
    "fidelityPoint": 42,
    "payment": 0,
    "account": "BKN1CST53"
  },
  {
    "id": 2,
    "firstName": "Michelle",
    "lastName": "Bigoudi",
    "fidelityPoint": 69,
    "payment": 3,
    "account": "BKN1BNT53"
  }
]
```

## Show one customer

Get the details of a customer registered in the CRM db with ID.

**Service name** : `crm`

**URL** : `/api/data/<id>`

**Method** : `GET`

**Auth required** : NO


**Success Response code:** `200 OK`

**Content examples:**


```json
 {
   "id": 1,
   "firstName": "Jacquie",
   "lastName": "Bloggs",
   "fidelityPoint": 42,
   "payment": 0,
   "account": "BKN1CST53"
 }
  
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
{
  "firstName": "Jacquie",
  "lastName": "Bloggs"
}
```
