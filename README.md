# CRM-app

This application manage all data from customers.

It includes:
 - firstName
 - lastName

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
    "lastName": "Bloggs"
  },
  {
    "id": 2,
    "firstName": "Michelle",
    "lastName": "Bigoudi"
  }
]
```
