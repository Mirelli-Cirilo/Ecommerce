from django.urls import path
from . import views


urlpatterns = [
    path('', views.LojaTemplateView.as_view(), name='loja'),
    path('carrinho/', views.CartTemplateView.as_view(), name='carrinho'),
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name="process_order"),
]

