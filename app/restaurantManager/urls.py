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

router.register('restaurant', views.RestaurantCRUDView)
# router.register('restaurants', views.RestaurantListView)

router.register('dish', views.DishView)
app_name = 'restaurantManager'

urlpatterns = [
    path('', include(router.urls))
]
