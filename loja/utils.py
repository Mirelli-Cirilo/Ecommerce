import json
from .models import *

def cookieCark(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
            cart = {}
    print('cart:', cart)         
    order = {'get_total_cart': 0, 'get_total_items':0}
    items = []
    cartItems = order['get_total_items']

    for i in cart:
        try:    
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]

            order['get_total_cart'] += total
            order['get_total_items'] += cart[i]["quantity"]

            item = {
                'product':{
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'imageURL': product.imageURL,
                },
                'quantity':cart[i]["quantity"],
                'get_total':total
            }
            items.append(item)
        except:
            pass
    return {'items': items, 'order': order, 'cartItems':cartItems}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_items
    else:
        cookieData = cookieCark(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'items': items, 'order': order, 'cartItems':cartItems}    

def guestOrder(request, data):
    print('User is not logged in')   
        
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCark(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order