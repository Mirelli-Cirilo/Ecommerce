from django.test import TestCase
from django.shortcuts import reverse
from django.db.models import QuerySet
from loja.models import *


class CartTemplateViewTestCaseUTils:
    URL = reverse('carrinho')
    TEMPLATE_NAME = 'loja/Carrinho.html'

    def _create_order(self):
        """
        Create an order with a customer. Every customer has a rel with an user
        """
        user = User.objects.create(username='test_user', password='123')
        customer = Customer.objects.create(user=user, name=user.username)
        order = Order.objects.create(customer=customer)

        return user, customer, order


class CartTemplateViewTestCase(TestCase, CartTemplateViewTestCaseUTils):
    def test_view_is_returning_correct_template(self):
        """
        Should return "loja/Carrinho.html" template to every request
        """
        response = self.client.get(self.URL)
        self.assertTemplateUsed(response, self.TEMPLATE_NAME)


    def test_view_is_returning_correct_value_in_context_order_for_authenticated_users(self):
        """
        Context "order" should return an instance of Order when user is authenticated
        """
        user, _, order = self._create_order()
        self.client.force_login(user)
        
        response = self.client.get(self.URL)
        context_order = response.context.get('order')

        self.assertIsInstance(context_order, Order)
        self.assertEqual(context_order.id, order.id)

    
    def test_view_is_returning_correct_value_in_context_order_for_unauthenticated_users(self):
        """
        Context "order" should return a dict when user is not authenticated
        """
        response = self.client.get(self.URL)
        context_order = response.context.get('order')
        EXPECTED_ORDER = {'get_total_cart':0, 'get_total_items':0}

        self.assertIsInstance(context_order, dict)
        self.assertEqual(context_order, EXPECTED_ORDER)
    
    
    def test_view_is_returning_correct_value_in_context_items_for_authenticated_users(self):
        """
        Context "item" should return a queryset
        """
        user, *_ = self._create_order()
        self.client.force_login(user)

        response = self.client.get(self.URL)
        context_item = response.context.get('items')

        self.assertIsInstance(context_item, QuerySet)
    

    def test_view_is_returning_correct_value_in_context_item_for_unauthenticated_users(self):
        """
        Context "items" should return an empty list when user is not authenticated
        """
        response = self.client.get(self.URL)
        context_item = response.context.get('items')

        self.assertIsInstance(context_item, list)


    def test_view_is_returning_correct_value_in_context_cartItem_for_authenticated_users(self):
        """
        Context "cartItems" should return an integer when user is authenticated
        """
        user, *_ = self._create_order()
        self.client.force_login(user)

        response = self.client.get(self.URL)
        context_cart_item = response.context.get('cartItems')
        
        self.assertIsInstance(context_cart_item, int)

        
    def test_view_is_returning_correct_value_in_context_cartItem_for_unauthenticated_users(self):
        """
        Context "cartItems" should return an integer when user is not authenticated
        """
        user, *_ = self._create_order()
        self.client.force_login(user)
        
        response = self.client.get(self.URL)
        conetxt_cart_item = response.context.get('cartItems')
        
        self.assertIsInstance(conetxt_cart_item, int)

