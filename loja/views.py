import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import *
from . import utils 


class LojaTemplateView(TemplateView):
    """
    This view return all products available
    """
    template_name = 'loja/Loja.html'

    def _get_cart_items(self):
        """
        Return cart items to be used in the view context
        """
        user = self.request.user
        if user.is_authenticated:
            kwargs = {'customer': user.customer, 'complete':False}
            return (
                Order.objects.get_or_create(**kwargs)[0]
                .get_total_items()
            )
        return utils.cookieCark(self.request).get('cartItems')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['cartItems'] = self._get_cart_items()
        return context


def carrinho(request):

    data = utils.cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'loja/Carrinho.html', context)

def checkout(request):

    data = utils.cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'loja/Checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print('productID', productID)
    print('action', action)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

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
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
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

