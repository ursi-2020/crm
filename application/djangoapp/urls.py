from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.customer, name='customer_list'),
    path('data/<slug:userId>', views.customer_by_ID, name='customer_by_id'),
    path('promotion', views.promo, name='promotion'),
    path('add_promotion/', views.add_promo, name='add_promotion'),
    path('test/', views.test, name='test'),
    path('update_db',views.update_db, name='update_db'),
    path('credit', views.credit, name='credit')

]
