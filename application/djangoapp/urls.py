from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('promotion', views.promo, name='promotion'),
    path('add_promotion/', views.add_promo, name='add_promotion'),
    path('test/', views.test, name='test'),
]