from django.db import models

class Truck(models.Model):
    name = models.CharField(max_length=255)

class FoodItemType(models.Model):
    name = models.CharField(max_length=255)

class FoodItem(models.Model):
    food_item_type = models.ForeignKey(FoodItemType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

class Order(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)