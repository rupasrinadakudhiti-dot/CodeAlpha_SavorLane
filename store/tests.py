from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Order, Product


class FoodOrderFlowTests(TestCase):
    def setUp(self):
        self.dish = Product.objects.create(name='Test Bowl', slug='test-bowl', category='Lunch', cuisine='Indian', description='Demo', ingredients='Rice', price='220.00', stock=4, dietary='VEG')
        self.user = User.objects.create_user(username='taster', password='StrongPass123!', email='taster@example.com')

    def test_catalog_filter(self):
        self.assertContains(self.client.get(reverse('products'), {'dietary': 'VEG'}), 'Test Bowl')
        self.assertNotContains(self.client.get(reverse('products'), {'dietary': 'VEGAN'}), 'Test Bowl')

    def test_order_requires_delivery_address_and_reduces_stock(self):
        self.client.force_login(self.user)
        self.client.post(reverse('cart_add', args=[self.dish.pk]), {'quantity': 2})
        data = {'full_name': 'Test Taster', 'email': 'taster@example.com', 'phone': '9999999999', 'fulfillment': 'DELIVERY', 'preferred_window': 'LUNCH'}
        response = self.client.post(reverse('checkout'), data)
        self.assertContains(response, 'Required for delivery.')
        self.assertFalse(Order.objects.exists())
        data.update(address='12 Test Road', city='Vijayawada', pincode='520001')
        response = self.client.post(reverse('checkout'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.get().items.count(), 1)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.stock, 2)

    def test_pickup_needs_no_delivery_address(self):
        self.client.force_login(self.user)
        self.client.post(reverse('cart_add', args=[self.dish.pk]), {'quantity': 1})
        response = self.client.post(reverse('checkout'), {'full_name': 'Test Taster', 'email': 'taster@example.com', 'phone': '9999999999', 'fulfillment': 'PICKUP', 'preferred_window': 'ASAP'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.get().fulfillment, 'PICKUP')
