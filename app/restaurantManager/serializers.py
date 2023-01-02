"""
Serializer for restaurant managment
"""

from core.models import Restaurant, Dish

from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'work_hours']
        read_only_fields = ['id']


class DishSerializer(serializers.ModelSerializer):
    """Serializers for dishes"""

    class Meta:
        model = Dish
        fields = ['id', 'name', 'category', 'ingredients', 'restaurant']
        read_only_fields = ['id']

    def create(self, validated_data):
        restaurants = Restaurant.objects.all().filter(
            user=validated_data['user']).order_by('-id')

        if (validated_data['restaurant'] not in restaurants):
            raise serializers.ValidationError(
                {"detail": "Restaurant does not belong to user"})

        dish = Dish(
            user=validated_data['user'],
            name=validated_data['name'],
            category=validated_data['category'],
            ingredients=validated_data['ingredients'],
            restaurant=validated_data['restaurant'],
        )
        dish.save()
        return dish
