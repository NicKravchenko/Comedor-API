"""
Serializer for restaurant managment
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from core.models import Restaurant

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _

class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ['id','name', 'location', 'work_hours']
        read_only_fields = ['id']