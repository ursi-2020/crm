from django.db import models
from datetime import datetime, timedelta, date

class Article(models.Model):
    nom = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)


class Vente(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return 'Vente: {} - {}'.format(self.article.nom, self.date)

class Customer(models.Model):
    IdClient = models.TextField(blank=False)
    Nom = models.CharField(max_length=200)
    Prenom = models.CharField(max_length=200)
    Credit = models.IntegerField(default=0)
    Date_paiement = models.DateField()
    Montant = models.IntegerField(default=0)
    NbRefus = models.IntegerField(default=0)
    Compte = models.CharField(max_length=10, default="")
    Age = models.IntegerField(default=-1)
    Sexe = models.CharField(max_length=5)
    Email = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)

class PurchasedArticle(models.Model):
    CodeProduit = models.CharField(max_length=200)
    Quantity = models.IntegerField(default=0)
    ticket = models.ForeignKey('Ticket', related_name='purchased_articles', on_delete=models.CASCADE)

class Ticket(models.Model):
    Date_ticket = models.DateField()
    prix = models.IntegerField(default=0)
    client = models.TextField(blank=False)
    Points_fidelite = models.IntegerField(default=0)
    Mode_paiement = models.CharField(max_length=10)
