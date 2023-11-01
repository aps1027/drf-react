from rest_framework import serializers
from .models import Order, Truck, FoodItemType, FoodItem, Flavor
 
 
def validate_truck_id(value):
    try:
        Truck.objects.get(pk=value)
    except Truck.DoesNotExist:
        raise serializers.ValidationError("Truck with this ID does not exist.")
    return value


def validate_food_item_type_id(value):
    try:
        FoodItemType.objects.get(pk=value)
    except FoodItemType.DoesNotExist:
        raise serializers.ValidationError("Food Item Type with this ID does not exist.")
    return value


class OrderSerializer(serializers.Serializer):
    food_item_type_id = serializers.IntegerField(validators=[validate_food_item_type_id])
    quantity = serializers.IntegerField()
    flavor_id = serializers.IntegerField(required=False)
    truck_id = serializers.IntegerField(validators=[validate_truck_id])


    def create(self):
        validated_data = self.validated_data

        quantity = validated_data['quantity']
        food_item_type_id = validated_data['food_item_type_id']
        flavor_id = validated_data.get('flavor_id')
        truck_id = validated_data['truck_id']

        food_item_type = FoodItemType.objects.get(pk=food_item_type_id)

        try:
            if food_item_type.has_flavor:
                if flavor_id is None:
                    raise serializers.ValidationError(
                        {'flavor_id': ['flavor_id is required for this food_item_type_id.']})
                food_item = FoodItem.objects.get(
                    truck=truck_id,
                    food_item_type=food_item_type_id,
                    fooditemflavor__flavor=flavor_id,
                )
            else:
                food_item = FoodItem.objects.get(
                    truck=truck_id,
                    food_item_type=food_item_type_id
                )
        except FoodItem.DoesNotExist:
            raise serializers.ValidationError({'message': 'UNAVAILABLE!'})

        if food_item.quantity >= quantity:
            food_item.quantity -= quantity
            food_item.save()
            order = Order(food_item=food_item, quantity=quantity, truck_id=truck_id)
            order.save()
        else:
            raise serializers.ValidationError({'message': 'SORRY!'})


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = '__all__'


class FoodItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItemType
        fields = '__all__'