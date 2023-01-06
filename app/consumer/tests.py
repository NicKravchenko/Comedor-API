from django.test import TestCase

from core.models import Restaurant, Dish
from consumer.serializers import RestaurantDishSerializer, RestaurantSerializer
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

# Create your tests here.
RESTAURANTS_URL = reverse('consumer:restaurant-list')
DISHES_LIST_URL = reverse('consumer:restaurant-dishes-list')


def create_user(email='user@example.com', password='password'):
    return get_user_model().objects.create(
        email=email,
        password=password,
        name='name'
    )


def create_restaurant(user, **kwargs):
    """Create restaurant"""
    restaurantData = {
        'name': 'name',
        'location': 'location',
        'work_hours': '12-20'
    }
    restaurantData.update(kwargs)
    restaurant = Restaurant.objects.create(user=user, **restaurantData)
    return restaurant


def create_dish(user, restaurant, **kwargs):
    """Create dish"""
    new_dish = {
        'name': 'name',
        'category': 'category',
        'ingredients': 'ingredientes'}
    new_dish.update(kwargs)

    dish = Dish.objects.create(user=user, restaurant=restaurant, **new_dish)
    return dish


class UnauthorizedUserTestCases(TestCase):

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_see_all_restaurants(self):
        """Test return all created restaurants"""
        create_restaurant(user=self.user)
        create_restaurant(user=self.user)

        res = self.client.get(RESTAURANTS_URL)

        restaurants = Restaurant.objects.all().order_by('-name')
        serializer = RestaurantSerializer(restaurants, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_see_dishes_of_the_restaurant(self):
        """Test that returned only dishes of selectioned restaurant"""
        restaurant1 = create_restaurant(user=self.user)
        restaurant2 = create_restaurant(user=self.user)

        create_dish(user=self.user, restaurant=restaurant1)
        create_dish(user=self.user, restaurant=restaurant1)

        create_dish(user=self.user, restaurant=restaurant2)
        dishes = Dish.objects.all() \
            .filter(restaurant=restaurant1) \
            .order_by('-name')
        serializedRestaurant = RestaurantDishSerializer(dishes, many=True)

        res = self.client.get(DISHES_LIST_URL, {'restaurant': restaurant1.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializedRestaurant.data)
        self.assertNotIn(restaurant2, res.data)
