"""
Views for consumers
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from rest_framework import mixins, viewsets

from core.models import Dish, Restaurant
from consumer import serializers


def _param_to_int(self, qs):
    """Convert parameter to an integer"""
    return int(qs)


class RestaurantListView(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Vieqw for list restaurants in api"""
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'restaurant',
                OpenApiTypes.STR,
                description='Comma separated list of tags ids to filter',
            )
        ]
    )
)
class DishOfRestaurantView(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """Vieqw for manage restaurant management api"""
    serializer_class = serializers.RestaurantDishSerializer
    queryset = Dish.objects.all()

    def get_queryset(self):
        """Show only restaurants of a person"""
        restaurant = self.request.query_params.get('restaurant')
        queryset = self.queryset
        if restaurant:
            queryset = queryset.filter(restaurant=restaurant).order_by('-name')

        return queryset
