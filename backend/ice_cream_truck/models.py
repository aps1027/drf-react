from django.db import models

class Truck(models.Model):
    name = models.CharField(max_length=255)

class FoodItemType(models.Model):
    name = models.CharField(max_length=255)
    has_flavor = models.BooleanField(default=False)

class FoodItem(models.Model):
    food_item_type = models.ForeignKey(FoodItemType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

class Flavor(models.Model):
    name = models.CharField(max_length=255)

class FoodItemFlavor(models.Model):
    flavor = models.ForeignKey(Flavor, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

class Order(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)