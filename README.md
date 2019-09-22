# CRM-app

This application manage all data from customers.

It includes:
 - firstName
 - lastName
 - fidelityPoint

# JSON API

## Show all customers

Get the details of all customers registered in the CRM db

**Service name** : `crm`

**URL** : `/customer`

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
    "fidelityPoint": 42
  },
  {
    "id": 2,
    "firstName": "Michelle",
    "lastName": "Bigoudi",
    "fidelityPoint": 69
  }
]
```

## Add a customer

Register a new customer in CRM db

**Service name** : `crm`

**URL** : `/customer`

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
