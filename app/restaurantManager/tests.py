from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Restaurant, Dish
from . import serializers

RESTAURANT_CRUD_URL = reverse('restaurantManager:restaurant-list')
DISH_CRUD_URL = reverse('restaurantManager:dish-list')
# RESTAURANT_LIST_URL = reverse('restaurantManager:restaurant-list')
# DISH_URL = reverse('restaurantManager:dish')


def create_user(**kargs):
    """Create user"""
    return get_user_model().objects.create_user(**kargs)


def create_restaurant(user, **params):
    """Create restaurant"""
    restaurantData = {
        'name': 'name',
        'location': 'location',
        'work_hours': '12-20'
    }
    restaurantData.update(params)

    restaurant = Restaurant.objects.create(user=user, **restaurantData)
    return restaurant


def create_dish(user, restaurant, **params):
    """Create dish"""
    dishData = {
        'name': 'name',
        'category': 'location',
        'ingredients': '12-20'
    }
    dishData.update(params)

    dish = Dish.objects.create(
        user=user, restaurant=restaurant, **dishData)
    return dish


class RestaurantManagmentTests(TestCase):
    """Tests for managing restaurant"""

    def setUp(self):
        self.client = APIClient()
        user_data = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        self.user = create_user(**user_data)
        self.client.force_authenticate(self.user)

    def test_create_restaurant(self):
        """Test for creating restaurant"""
        payload = {
            'name': 'name',
            'location': 'location',
            'work_hours': '12-20'
        }

        res = self.client.post(RESTAURANT_CRUD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_users_restaurant(self):
        """Test for getting restaurant created by user"""
        restaurantData = {
            'name': 'name',
            'location': 'location',
            'work_hours': '12-20',
            'user': self.user
        }

        restaurantRes = self.client.post(RESTAURANT_CRUD_URL, restaurantData)

        payload = {
            'id': restaurantRes.data['id']
        }
        res = self.client.get(RESTAURANT_CRUD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_other_users_restaurant_not_allowed(self):
        """Test for getting restaurant created by user"""
        restaurantData = {
            'name': 'newname',
            'location': 'location',
            'work_hours': '12-20',
            'user': self.user
        }

        newUser = create_user(email='newuser@example.com', password='password')

        self.client.post(RESTAURANT_CRUD_URL, restaurantData)
        restarant2 = create_restaurant(user=newUser)

        restaurnatsOfUser = Restaurant.objects.filter(user=self.user)
        serializer = serializers.RestaurantSerializer(
            restaurnatsOfUser, many=True)

        res = self.client.get(RESTAURANT_CRUD_URL)

        self.assertEqual(res.data, serializer.data)
        self.assertNotIn(restarant2, res.data)


class DishManagmentTests(TestCase):
    """Tests for managing restaurant"""

    def setUp(self):
        self.client = APIClient()
        user_data = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        self.user = create_user(**user_data)
        self.client.force_authenticate(self.user)

    def test_show_only_dish_of_user(self):
        """Test show only dish of user"""
        new_user = create_user(
            email='newuser@example.com', password='password')

        restaurant1 = create_restaurant(user=self.user)
        restaurant2 = create_restaurant(user=new_user)

        create_dish(user=self.user, restaurant=restaurant1)
        dish2 = create_dish(user=new_user, restaurant=restaurant2)

        dishOfUser = Dish.objects.filter(user=self.user)
        dishSerialized = serializers.DishSerializer(dishOfUser, many=True)

        res = self.client.get(DISH_CRUD_URL)

        self.assertEqual(res.data, dishSerialized.data)
        self.assertNotIn(dish2, res.data)

    def test_assign_dish_to_owners_restaurant(self):
        """Test assign dish to owners restaurant"""
        restaurant = create_restaurant(user=self.user)
        payload = {
            'name': 'name',
            'category': 'location',
            'ingredients': '12-20',
            'restaurant': restaurant.id
        }

        res = self.client.post(DISH_CRUD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_assign_dish_not_to_owners_restaurant(self):
        """Test assign dish to other \\
            owner restaurant not work but to owners yes"""
        new_user = create_user(
            email='newuser@example.com',
            password='password'
        )
        restaurant1 = create_restaurant(user=self.user)
        restaurant2 = create_restaurant(user=new_user)
        payload1 = {
            'name': 'name',
            'category': 'location',
            'ingredients': '12-20',
            'restaurant': restaurant2.id
        }
        payload2 = {
            'name': 'name',
            'category': 'location',
            'ingredients': '12-20',
            'restaurant': restaurant1.id
        }

        res1 = self.client.post(DISH_CRUD_URL, payload1)
        res2 = self.client.post(DISH_CRUD_URL, payload2)

        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
