import json
from .models import *


def cookieCark(request):
    cart = request.COOKIES.get('cart', {})

    if cart != {}: 
        cart = json.loads(cart)

    order = {'get_total_cart':0, 'get_total_items':0}
    items = []
    cartItems = order['get_total_items']

    for i in cart:
        try:    
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]
            
            order['get_total_cart'] += total
            order['get_total_items'] += cart[i]["quantity"]

            items.append({
                'product':product.to_dict(),
                'quantity':cart[i]["quantity"],
                'get_total':total
            })

        except:
            pass

    return {'items':items, 'order':order, 'cartItems':cartItems}


def guestOrder(request, data):
    print('User is not logged in')   
        
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCark(request)
    items = cookieData['items']

    customer = Customer.objects.get_or_create(email=email)[0]
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order


class TemplateViewUtils:
    def get_data(self):
        user = self.request.user

        if user.is_authenticated:
            data = dict()
            kwargs = {'customer':user.customer, 'complete':False}
            data['order'] = Order.objects.get_or_create(**kwargs)[0]
            data['items'] = data['order'].orderitem_set.all()
            data['cartItems'] = data['order'].get_total_items
            return data

        return cookieCark(self.request)

