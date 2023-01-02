""" 
URL mappings for restaurant managment app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from restaurantManager import views

router = DefaultRouter()

router.register('restaurant', views.RestaurantCRUDView, basename='restaurant-crud')
router.register('restaurant-list', views.RestaurantListView, basename='restaurant-list')

router.register('dish', views.DishView)
app_name = 'restaurantManager'

urlpatterns = [
    path('', include(router.urls))
]