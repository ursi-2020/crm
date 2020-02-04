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
    Date_paiement = models.DateField(null=True)
    Montant = models.IntegerField(default=0)
    NbRefus = models.IntegerField(default=0)
    Compte = models.CharField(max_length=10, default="")
    Age = models.IntegerField(default=-1)
    Sexe = models.CharField(max_length=5, default="")
    Email = models.CharField(max_length=200)
    Phone = models.CharField(max_length=200)
    PanierMoyen = models.IntegerField(default=0)

class PurchasedArticle(models.Model):
    codeProduit = models.CharField(max_length=200)
    prixAvant = models.IntegerField(default=0)
    prixApres = models.IntegerField(default=0)
    promo = models.IntegerField(default=0)
    promo_client_produit = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    ticket = models.ForeignKey('Ticket', related_name='purchased_articles', on_delete=models.CASCADE)

class Ticket(models.Model):
    uid = models.TextField(blank=False, primary_key=True)
    DateTicket = models.DateField(blank=True, null=True)
    Prix = models.IntegerField(default=0)
    Client = models.TextField(blank=False)
    PointsFidelite = models.IntegerField(default=0)
    ModePaiement = models.CharField(max_length=10)
    SendedBi = models.BooleanField(default=False)
    SendedPromo = models.BooleanField(default=False)
    Origin = models.TextField(blank=False)
    Promo_client = models.IntegerField(default=0)
