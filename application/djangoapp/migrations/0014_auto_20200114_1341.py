# Generated by Django 3.0.1 on 2020-01-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0013_auto_20191213_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='PanierMoyen',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ticket',
            name='Origin',
            field=models.TextField(default='e-commerce'),
            preserve_default=False,
        ),
    ]