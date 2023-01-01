"""
Views for the user API
"""
from rest_framework import generics

from user.serializers import userSerializer


class CreateUserView(generics.CreateAPIView):
    """Createa a new user"""
    serializer_class = userSerializer
