from django.urls import path

from . import views

urlpatterns = [
    path('customer/', views.customer, name='customer'),
    path('creation/', views.create, name='creation'),

]