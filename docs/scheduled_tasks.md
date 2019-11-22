# Scheduled tasks

## Add credit of magasin
This task get all tickets of the day from gestion-magasin, save them and compute credit which is 0,5% of total amount

**Name:** `CRM-credit-clients`

**Recurence:** `day` 

## Add credit of e-commerce
This task get all tickets of the day from e-commerce, save them and compute credit which is 0,5% of total amount

**Name:** `CRM-credit-clients-ecommerce`

**Recurence:** `day` 

## Deferred payment
This task check all deferred payment which should be paid at the scheduler date and send payment to gestion-paiement

**Name:** `CRM-schedule-paiement`

**Recurence:** `day` 
