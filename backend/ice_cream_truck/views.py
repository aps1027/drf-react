from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FoodItem, Truck, Order, FoodItemType, Flavor
from .serializer import OrderSerializer, TruckSerializer, FlavorSerializer, FoodItemTypeSerializer
from rest_framework import status

@api_view(['POST'])
def postOrder(request):
    """
    Create a new order for a specific food item from the ice cream truck.

    URL:
        http://localhost:8000/api/order/

    Args:
        food_item_type_id: Food Item Type ID
        quantity: quantity 
        flavor_id: Flavor ID (optional for food item that does not have flavor)
        truck_id: Truck ID

    Returns:
        "ENJOY!": if buy in stock amount of food
        "SORRY!": if buy out of stock amount of food
    """
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.create()
        return Response({'message': 'ENJOY!'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getTruckDetail(request, pk):
    """
    Get details of a specific ice cream truck, including its food items and total earnings.

    URL:
        http://localhost:8000/api/truck/<pk>

    Args:
        pk (int): The primary key of the truck to retrieve details.

    Returns:
        A JSON response with the truck's details.
    """
    try:
        truck = Truck.objects.get(pk=pk)
        food_items = FoodItem.objects.filter(truck=truck)
        food_items_list = []

        for item in food_items:
            flavors = [flavor.flavor.name for flavor in item.fooditemflavor_set.all()]
            food_item_data = {
                'id': item.id,
                'type': item.food_item_type.name,
                'flavor': flavors[0] if len(flavors) else '',
                'price': item.price,
                'quantity': item.quantity
            }
            food_items_list.append(food_item_data)

        orders = Order.objects.filter(truck=truck)
        total_amount = sum(order.food_item.price * order.quantity for order in orders)

        return Response({
            'id': truck.id,
            'name': truck.name,
            'food_items': food_items_list,
            'total_amount': total_amount
        })
    except Truck.DoesNotExist:
        return Response({'detail': 'Truck not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def getTrucks(request):
    """
    Get truck list

    URL:
        http://localhost:8000/api/truck/

    Returns:
        A JSON response with the truck list.
    """
    trucks = Truck.objects.all()
    serializer = TruckSerializer(trucks, many=True)
    return Response({ 'trucks': serializer.data })

@api_view(['GET'])
def getFlavors(request):
    """
    Get flavor list

    URL:
        http://localhost:8000/api/flavor/

    Returns:
        A JSON response with the flavor list.
    """
    flavors = Flavor.objects.all()
    serializer = FlavorSerializer(flavors, many=True)
    return Response({ 'flavors': serializer.data })

@api_view(['GET'])
def getFoodItemTypes(request):
    """
    Get food item type list

    URL:
        http://localhost:8000/api/food-item-type/

    Returns:
        A JSON response with the food item type list.
    """
    food_item_types = FoodItemType.objects.all()
    serializer = FoodItemTypeSerializer(food_item_types, many=True)
    return Response({ 'food_item_types': serializer.data })