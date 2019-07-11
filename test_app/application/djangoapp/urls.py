from django.urls import path

from . import views

urlpatterns = [
    path('customers', views.getCustomerInfo, name='customer_info'),
    path('create_customer', views.creatCustomer, name='create_customer'),
]