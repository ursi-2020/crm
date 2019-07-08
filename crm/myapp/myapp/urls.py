from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer', views.getCustomerInfo, name='customer'),
    path('create_customer', views.creatCustomer, name='create_customer'),
]