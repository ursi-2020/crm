# Generated by Django 3.0.3 on 2020-02-03 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('stock', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdClient', models.TextField()),
                ('Nom', models.CharField(max_length=200)),
                ('Prenom', models.CharField(max_length=200)),
                ('Credit', models.IntegerField(default=0)),
                ('Date_paiement', models.DateField(null=True)),
                ('Montant', models.IntegerField(default=0)),
                ('NbRefus', models.IntegerField(default=0)),
                ('Compte', models.CharField(default='', max_length=10)),
                ('Age', models.IntegerField(default=-1)),
                ('Sexe', models.CharField(default='', max_length=5)),
                ('Email', models.CharField(max_length=200)),
                ('Phone', models.CharField(max_length=200)),
                ('PanierMoyen', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('uid', models.TextField(primary_key=True, serialize=False)),
                ('DateTicket', models.DateField(blank=True, null=True)),
                ('Prix', models.IntegerField(default=0)),
                ('Client', models.TextField()),
                ('PointsFidelite', models.IntegerField(default=0)),
                ('ModePaiement', models.CharField(max_length=10)),
                ('SendedBi', models.BooleanField(default=False)),
                ('SendedPromo', models.BooleanField(default=False)),
                ('Origin', models.TextField()),
                ('CustomerPromo', models.IntegerField(default=0)),
                ('GlobalPromo', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.Article')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeProduit', models.CharField(max_length=200)),
                ('prixAvant', models.IntegerField(default=0)),
                ('prixApres', models.IntegerField(default=0)),
                ('promo', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_articles', to='djangoapp.Ticket')),
            ],
        ),
    ]
