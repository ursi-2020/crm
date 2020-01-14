from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.customer, name='customer_list'),
    path('data/<slug:userId>', views.customer_by_ID, name='customer_by_id'),
    path('customer/email', views.customer_by_email, name='customer_by_email'),
    path('promotion', views.promo, name='promotion'),
    path('add_promotion/', views.add_promo, name='add_promotion'),
    path('test/', views.test, name='test'),
    path('update_db',views.update_db, name='update_db'),
    path('credit', views.credit, name='credit'),
    path('credit_ecommerce', views.credit_ecommerce, name='credit_ecommerce'),
    path('credit/<int:idClient>', views.getCredit, name='get_credit'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('allow_credit', views.allow_credit, name='allow_credit'),
    path('get_tickets', views.get_tickets, name='get_tickets'),
    path('paiement', views.paiement, name='paiement'),
    path('test_tickets', views.test_tickets, name='test_tickets'),
    path('create_customer_with_id_test', views.create_customer_with_id_test, name='create_customer_with_id_test'),
    path('generate_tickets', views.generate_tickets, name='generate_tickets'),

]
