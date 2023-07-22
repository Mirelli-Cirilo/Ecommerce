import json
import datetime
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import *
from . import utils 


class CustomAbstractTemplateView(TemplateView, utils.TemplateViewUtils):
    """
    An abstract view that join TemplateView and utils.TemplateViewUtils 
    and implements "get_context_data" method.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_data()
        return {**data, **context}


class LojaTemplateView(CustomAbstractTemplateView):
    """
    This view return all products available
    """
    template_name = 'loja/Loja.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['cartItems'] = self.get_data().get('cartItems')
        return context


class CartTemplateView(CustomAbstractTemplateView):
    template_name = 'loja/Carrinho.html'


class CheckoutTemplateView(CustomAbstractTemplateView):
    template_name = 'loja/Checkout.html'


def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('productID', productID)
    print('action', action)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order = Order.objects.get_or_create(customer=customer, complete=False)[0]

    orderItem = OrderItem.objects.get_or_create(order=order, product=product)[0]

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()  

    if orderItem.quantity <= 0:
        orderItem.delete()  

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order = Order.objects.get_or_create(customer=customer, complete=False)[0]
	else:
		customer, order = utils.guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_total_cart):
		order.complete = True
	order.save()

	if data['shipping'] != '':
		ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            cep=data['shipping']['cep'],
	    )

	return JsonResponse('Payment submitted..', safe=False) 

