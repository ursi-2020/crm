from django.urls import path

from . import views

urlpatterns = [
    path('customer/', views.customer, name='customer'),
    path('promotion/', views.promo, name='promotion'),
    path('add_promotion/', views.add_promo, name='add_promotion'),

]