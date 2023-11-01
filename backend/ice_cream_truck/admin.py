from django.contrib import admin
from .models import Truck, FoodItemType, FoodItem, Order, Flavor, FoodItemFlavor

admin.site.register([Truck, FoodItemType, FoodItem, Order, Flavor, FoodItemFlavor])