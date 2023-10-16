from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FoodItem, Truck, Order
from .serializer import OrderSerializer
from rest_framework import status

@api_view(['POST'])
def postOrder(request):
    """
    Create a new order for a specific food item from the ice cream truck.

    URL:
        http://localhost:8000/api/order/

    Args:
        food_item: Food Item ID
        quantity: quantity 
        truck: Truck ID

    Returns:
        "ENJOY!": if buy in stock amount of food
        "SORRY!": if buy out of stock amount of food
    """
    serializer = OrderSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    quantity = int(request.data['quantity'])
    food_item_id = request.data['food_item']
    food_item = FoodItem.objects.get(id=food_item_id)
    if food_item.quantity >= quantity:
        food_item.quantity -= quantity
        food_item.save()
        serializer.save()
        return Response({'message': 'ENJOY!'})
    else:
        return Response({'message': 'SORRY!'}, status=status.HTTP_400_BAD_REQUEST)

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
        food_items = [
                {
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'quantity': item.quantity
                }
                for item in food_items
            ]

        orders = Order.objects.filter(truck=truck)
        total_amount = sum(order.food_item.price * order.quantity for order in orders)

        return Response({
            'id': truck.id,
            'name': truck.name,
            'food_items': food_items, 
            'total_amount': total_amount})
    except Truck.DoesNotExist:
        return Response({'detail': 'Truck not found'}, status=status.HTTP_404_NOT_FOUND)