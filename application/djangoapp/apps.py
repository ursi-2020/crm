import os

from django.apps import AppConfig
from apipkg import api_manager as api
from datetime import datetime, timedelta

myappurl = "http://localhost:" + os.environ["WEBSERVER_PORT"]


def schedule_allowed_payment(time):
    target_app = 'crm'
    target_url = 'api/paiement'
    data = '{}'
    source_app = "crm"
    name = "CRM-schedule-paiement"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_credit(time):
    target_app = 'crm'
    target_url = 'api/credit'
    data = '{}'
    source_app = "crm"
    name = "CRM-credit-clients"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

def schedule_credit_ecommerce(time):
    target_app = 'crm'
    target_url = 'api/credit_ecommerce'
    data = '{}'
    source_app = "crm"
    name = "CRM-credit-clients-ecommerce"
    api.schedule_task(target_app, target_url, time, 'day', data, source_app, name)

class ApplicationConfig(AppConfig):
    name = 'application.djangoapp'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            api.unregister(os.environ['DJANGO_APP_NAME'])
            api.register(myappurl, os.environ['DJANGO_APP_NAME'])

            clock_time = api.send_request('scheduler', 'clock/time')
            time = datetime.strptime(clock_time, '"%d/%m/%Y-%H:%M:%S"')
            time = time + timedelta(seconds=180)
            schedule_allowed_payment(time)
            #schedule_credit(time)
            #schedule_credit_ecommerce(time)
