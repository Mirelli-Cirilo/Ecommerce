from django.urls import path
from . import views

urlpatterns = [
    path('', views.loja, name='loja'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name="process_order"),
]