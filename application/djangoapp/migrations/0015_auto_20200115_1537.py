# Generated by Django 3.0.1 on 2020-01-15 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0014_auto_20200114_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='SendedBi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='SendedPromo',
            field=models.BooleanField(default=False),
        ),
    ]
