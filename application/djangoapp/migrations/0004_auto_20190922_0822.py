# Generated by Django 2.2.5 on 2019-09-22 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0003_auto_20190922_0802'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='Account',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='Payment',
            new_name='payment',
        ),
    ]