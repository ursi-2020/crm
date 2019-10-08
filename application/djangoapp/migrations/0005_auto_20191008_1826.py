# Generated by Django 2.2.6 on 2019-10-08 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0004_auto_20190922_0822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='account',
            new_name='Compte',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='firstName',
            new_name='Nom',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='fidelityPoint',
            new_name='Paiement',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='lastName',
            new_name='Prenom',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='payment',
        ),
        migrations.AddField(
            model_name='customer',
            name='Credit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='customer',
            name='IdClient',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]