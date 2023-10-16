from django.urls import path
from . import views
urlpatterns = [
    path('order/', views.postOrder, name="order"),
    path('truck/<int:pk>', views.getTruckDetail, name="truck-detail"),
]
