# Generated by Django 2.2.6 on 2019-10-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0005_auto_20191008_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='carteFid',
            field=models.IntegerField(default=-1),
        ),
    ]
