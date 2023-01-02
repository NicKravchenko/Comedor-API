""" 
URL mappings for restaurant managment app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from restaurant import views

router = DefaultRouter()

router.register('list', views.ListRestaurantView)
router.register('', views.CRUDRestaurantView)
app_name = 'restaurant'

urlpatterns = [
    path('', include(router.urls))
]