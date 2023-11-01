from django.test import TestCase
from rest_framework.test import APIClient
from .models import FoodItem, Truck, FoodItemType, Flavor, FoodItemFlavor
from decimal import Decimal
from django.urls import reverse


class IceCreamTruckTests(TestCase):


    def setUp(self):
        self.truck_A = Truck.objects.create(name='Truck A')
        self.truck_B = Truck.objects.create(name='Truck B')

        self.chocolate_flavor = Flavor.objects.create(name='Chocolate')
        self.pistachio_flavor = Flavor.objects.create(name='Pistachio')
        self.strawberry_flavor = Flavor.objects.create(name='Strawberry')
        self.mint_flavor = Flavor.objects.create(name='Mint')

        self.ice_cream_type = FoodItemType.objects.create(name='Ice Cream', has_flavor=True)
        self.shaved_ice_type = FoodItemType.objects.create(name='Shaved Ice')
        self.snack_bar_type = FoodItemType.objects.create(name='Snack Bar')

        self.chocolate_ice_cream = FoodItem.objects.create(
            food_item_type=self.ice_cream_type,
            price=Decimal('10.00'),
            quantity=10,
            truck=self.truck_A
        )
        FoodItemFlavor.objects.create(food_item=self.chocolate_ice_cream, flavor=self.chocolate_flavor)

        self.pistachio_ice_cream = FoodItem.objects.create(
            food_item_type=self.ice_cream_type,
            price=Decimal('10.00'),
            quantity=10,
            truck=self.truck_A
        )
        FoodItemFlavor.objects.create(food_item=self.pistachio_ice_cream, flavor=self.pistachio_flavor)

        self.shaved_ice = FoodItem.objects.create(
            food_item_type=self.shaved_ice_type,
            price=Decimal('8.00'),
            quantity=10,
            truck=self.truck_A
        )

        self.client = APIClient()


    def test_unavailable_food_item_type_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': 9999,
            'quantity': 1,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(
            order_response.data['food_item_type_id'][0], 'Food Item Type with this ID does not exist.')
        

    def test_unavailable_truck_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.snack_bar_type.id,
            'quantity': 1,
            'truck_id': 9999,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(
            order_response.data['truck_id'][0], 'Truck with this ID does not exist.')


    def test_ice_cream_order_without_flavor_id(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.ice_cream_type.id,
            'quantity': 1,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(
            order_response.data['flavor_id'][0], 'flavor_id is required for this food_item_type_id.')


    def test_instock_chocolate_ice_cream_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.ice_cream_type.id,
            'quantity': 5,
            'flavor_id': self.chocolate_flavor.id,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 200)
        self.assertEqual(order_response.data['message'], 'ENJOY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_A.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], \
                         self.chocolate_ice_cream.price * test_data['quantity'])


    def test_out_of_stock_chocolate_ice_cream_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.ice_cream_type.id,
            'quantity': 11,
            'flavor_id': self.chocolate_flavor.id,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(order_response.data['message'], 'SORRY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_A.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], 0)


    def test_unavailable_mint_ice_cream_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.ice_cream_type.id,
            'quantity': 11,
            'flavor_id': self.mint_flavor.id,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(order_response.data['message'], 'UNAVAILABLE!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_A.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], 0)


    def test_instock_shaved_ice_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.shaved_ice_type.id,
            'quantity': 5,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 200)
        self.assertEqual(order_response.data['message'], 'ENJOY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_A.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], \
                         self.shaved_ice.price * test_data['quantity'])


    def test_out_of_stock_shaved_ice_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.shaved_ice_type.id,
            'quantity': 11,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(order_response.data['message'], 'SORRY!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_A.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], 0)

    
    def test_unavailable_snack_bar_order(self):
        order_url = reverse('order')
        test_data = {
            'food_item_type_id': self.snack_bar_type.id,
            'quantity': 1,
            'truck_id': self.truck_A.id,
        }
        order_response = self.client.post(order_url, test_data)
        self.assertEqual(order_response.status_code, 400)
        self.assertEqual(order_response.data['message'], 'UNAVAILABLE!')

        truck_detail_url = reverse('truck-detail', kwargs={'pk': self.truck_A.id})
        truck_response = self.client.get(truck_detail_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(truck_response.data['total_amount'], 0)

    
    def test_get_trucks(self):
        truck_list_url = reverse('truck-list')
        truck_response = self.client.get(truck_list_url)
        self.assertEqual(truck_response.status_code, 200)
        self.assertEqual(len(truck_response.data['trucks']), 2)
        self.assertEqual(truck_response.data['trucks'][0]['name'], 'Truck A')
        self.assertEqual(truck_response.data['trucks'][1]['name'], 'Truck B')

    
    def test_get_flavors(self):
        flavor_list_url = reverse('flavor-list')
        flavor_response = self.client.get(flavor_list_url)
        self.assertEqual(flavor_response.status_code, 200)
        self.assertEqual(len(flavor_response.data['flavors']), 4)
        self.assertEqual(flavor_response.data['flavors'][0]['name'], 'Chocolate')
        self.assertEqual(flavor_response.data['flavors'][1]['name'], 'Pistachio')
        self.assertEqual(flavor_response.data['flavors'][2]['name'], 'Strawberry')
        self.assertEqual(flavor_response.data['flavors'][3]['name'], 'Mint')

    
    def test_get_food_item_types(self):
        type_list_url = reverse('food-item-type-list')
        type_response = self.client.get(type_list_url)
        self.assertEqual(type_response.status_code, 200)
        self.assertEqual(len(type_response.data['food_item_types']), 3)
        self.assertEqual(type_response.data['food_item_types'][0]['name'], 'Ice Cream')
        self.assertEqual(type_response.data['food_item_types'][1]['name'], 'Shaved Ice')
        self.assertEqual(type_response.data['food_item_types'][2]['name'], 'Snack Bar')
