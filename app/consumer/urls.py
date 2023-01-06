from django.urls import (
    path,
    include,
)
from consumer.views import DishOfRestaurantView, RestaurantListView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'restaurant', RestaurantListView)
router.register(r'restaurant-dishes',
                DishOfRestaurantView,
                basename='restaurant-dishes'
                )

app_name = 'consumer'

urlpatterns = [
    path('', include(router.urls))
]
