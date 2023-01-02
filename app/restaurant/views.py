"""
Views for restaurant managment api
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Restaurant
from restaurant import serializers

class RestaurantViewSet(viewsets.ModelViewSet):
    """Vieqw for manage restaurant management api"""
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Show only restaurants of a person"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
class ListRestaurantView(
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Vieqw for manage restaurant management api"""
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()
    
class CRUDRestaurantView(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Vieqw for manage restaurant management api"""
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Show only restaurants of a person"""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    