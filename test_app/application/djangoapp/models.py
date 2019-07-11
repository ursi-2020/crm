from django.db import models


class Customer(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    fidelityPoint = models.IntegerField()
