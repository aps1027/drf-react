from django.urls import path
from . import views
urlpatterns = [
    path('order/', views.postOrder, name="order"),
    path('truck/', views.getTrucks, name="truck-list"),
    path('truck/<int:pk>', views.getTruckDetail, name="truck-detail"),
    path('flavor/', views.getFlavors, name="flavor-list"),
    path('food-item-type/', views.getFoodItemTypes, name="food-item-type-list"),
]
