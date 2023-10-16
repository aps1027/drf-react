from django.contrib import admin
from .models import Truck, FoodItemType, FoodItem, Order

admin.site.register([Truck, FoodItemType, FoodItem, Order])