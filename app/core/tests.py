from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='password'):
    return get_user_model().objects.create_user(email, password)


class ModelCreationTestCase(TestCase):
    """Testing models"""

    def test_create_user_with_email_succesfull(self):
        """Test create a user with an email succesfull"""
        email = 'test@example.com'
        password = 'pasword'

        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_restaurant(self):
        """Test create restaurant"""
        user = create_user()

        restaurant = models.Restaurant.objects.create(
            name='name',
            location='location',
            work_hours='20-22',
            user=user
        )

        self.assertEqual(str(restaurant), restaurant.name)

    def test_create_dish(self):
        """Test create dish"""
        user = create_user()
        restaurant = models.Restaurant.objects.create(
            name='name',
            location='location',
            work_hours='20-22',
            user=user
        )

        dish = models.Dish.objects.create(
            name='name',
            category='category',
            ingredients='ingredients',
            user=user,
            restaurant=restaurant
        )

        self.assertEqual(str(dish), dish.name)
