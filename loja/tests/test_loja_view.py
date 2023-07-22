from django.test import TestCase
from django.shortcuts import reverse
from django.db.models import QuerySet
from loja.models import Product


class LojaTemplateViewTestCaseUtils:
    URL = reverse('loja')
    TEMPLATE_NAME = 'loja/Loja.html'
 
    def _create_products(self, number_of_products):
        Product.objects.bulk_create([
            Product(name=f'Prod Test {i}', price=i/2)
            for i in range(number_of_products)
        ])


class LojaTemplateViewTestCase(TestCase, LojaTemplateViewTestCaseUtils):
    def test_view_is_using_correct_template(self):
        """
        Should return "loja/Loja.html" template to every request
        """
        response = self.client.get(self.URL)
        self.assertTemplateUsed(response, self.TEMPLATE_NAME)
    

    def test_view_is_returning_correct_value_for_context_cartItem(self):
        """
        Should return an integer with the number of items added to cart
        """
        response = self.client.get(self.URL)

        cart_items = response.context.get('cartItems')
        NUMBER_OF_CART_ITEMS = 0

        self.assertIsInstance(cart_items, int)
        self.assertEqual(NUMBER_OF_CART_ITEMS, cart_items)


    def test_view_is_returning_correct_values_for_context_products(self):
        """
        Should return a queryset containing all products available
        """
        NUMBER_OF_PRODUCTS = 10
        self._create_products(NUMBER_OF_PRODUCTS)

        response = self.client.get(self.URL)
        products = response.context.get('products')

        self.assertIsInstance(products, QuerySet)
        self.assertEqual(products.count(), NUMBER_OF_PRODUCTS)

