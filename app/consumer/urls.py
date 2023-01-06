from django.urls import (
    path,
    include,
)
from consumer.views import DishOfRestaurantView, RestaurantListView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('restaurant', RestaurantListView)
router.register('restaurant-dish', DishOfRestaurantView)

app_name = 'consumer'

urlpatterns = [
    path('', include(router.urls))
]
