"""
Serializers for consumer app
"""

from core.models import Restaurant, Dish

from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'work_hours']
        read_only_fields = ['id']


class RestaurantDishSerializer(serializers.ModelSerializer):
    """Serializers for dishes"""

    class Meta:
        model = Dish
        fields = ['id', 'name', 'category', 'ingredients', 'restaurant']
        read_only_fields = ['id']
