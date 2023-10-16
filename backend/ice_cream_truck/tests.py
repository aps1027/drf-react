from django.test import TestCase
from rest_framework.test import APIClient
from .models import FoodItem, Truck, FoodItemType
from decimal import Decimal
from django.urls import reverse

class IceCreamTruckTests(TestCase):
    def setUp(self):
        self.truck_1 = Truck.objects.create(name='Truck 1')

        self.food_item_type_1 = FoodItemType.objects.create(name='Ice Cream')
        self.food_item_type_2 = FoodItemType.objects.create(name='Shaved Ice')

        self.truck_1_food_item_1 = FoodItem.objects.create(
            food_item_type=self.food_item_type_1,
            name='Chocolate Ice Cream',
            price=Decimal('10.00'),
            quantity=10,
            truck=self.truck_1
        )
        self.truck_1_food_item_2 = FoodItem.objects.create(
            food_item_type=self.food_item_type_1,
            name='Strawberry Ice Cream',
            price=Decimal('5.00'),
            quantity=10,
            truck=self.truck_1
        )

        self.truck_1_food_item_3 = FoodItem.objects.create(
            food_item_type=self.food_item_type_2,
            name='Shaved Ice - Lemon',
            price=Decimal('15.00'),
            quantity=10,
            truck=self.truck_1
        )
        self.truck_1_food_item_4 = FoodItem.objects.create(
            food_item_type=self.food_item_type_2,
            name='Shaved Ice - Grape',
            price=Decimal('20.00'),
            quantity=10,
            truck=self.truck_1
        )

        self.client = APIClient()

    def test_single_order_for_in_stock_quantity(self):
        order_url = reverse('order')
        test_data = {
            'food_item': self.truck_1_food_item_1.id,
            'quantity': 5,
            'truck': self.truck_1.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 200)
        self.assertEqual(order_response.data['message'], 'ENJOY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_1.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], \
                         self.truck_1_food_item_1.price * test_data['quantity'])
    
    def test_multiple_order_for_in_stock_quantity(self):
        order_url = reverse('order')
        ice_cream_test_data = {
            'food_item': self.truck_1_food_item_1.id,
            'quantity': 5,
            'truck': self.truck_1.id,
        }
        ice_cream_order_response = self.client.post(order_url, ice_cream_test_data)
        self.assertEqual(ice_cream_order_response.status_code, 200)
        self.assertEqual(ice_cream_order_response.data['message'], 'ENJOY!')

        shaved_ice_test_data = {
            'food_item': self.truck_1_food_item_3.id,
            'quantity': 5,
            'truck': self.truck_1.id,
        }
        shaved_ice_order_response = self.client.post(order_url, shaved_ice_test_data)
        self.assertEqual(shaved_ice_order_response.status_code, 200)
        self.assertEqual(shaved_ice_order_response.data['message'], 'ENJOY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_1.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], \
                         (self.truck_1_food_item_1.price * ice_cream_test_data['quantity']) \
                            + (self.truck_1_food_item_3.price * shaved_ice_test_data['quantity']))
        
    def test_order_for_out_of_stock_quantity(self):
        order_url = reverse('order')
        test_data = {
            'food_item': self.truck_1_food_item_1.id,
            'quantity': 11,
            'truck': self.truck_1.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(order_response.data['message'], 'SORRY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_1.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], 0)

