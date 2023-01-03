from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kargs):
    return get_user_model().objects.create_user(**kargs)


class PublicUserAPITests(TestCase):
    """Test for unauthorized users"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test create user is successfull"""

        payload = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', res.data)

    def test_create_user_with_existing_mail(self):
        """Test create user is unsuccessfull with existing mail"""
        payload = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_mail(self):
        """Test create user is unsuccessfull with no mail"""
        payload = {
            'email': '',
            'password': 'password',
            'name': 'name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_no_password(self):
        """Test create user is unsuccessfull with no password"""
        payload = {
            'email': 'user@example.com',
            'password': '',
            'name': 'name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test create token by credential for existing user"""
        user = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        create_user(**user)

        payload = {
            'email': user['email'],
            'password': user['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_wrong_user(self):
        """Test create token by credential for not existing user"""
        user = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        create_user(**user)

        payload = {
            'email': 'user1@example.com',
            'password': user['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_wrong_password_user(self):
        """Test create token by credential for not existing user"""
        user = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        create_user(**user)

        payload = {
            'email': user['email'],
            'password': 'password1'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertNotEqual(res.status_code, status.HTTP_200_OK)


class AuthorizedUserAPITests(TestCase):
    """Test for authorized users"""

    def setUp(self):
        self.client = APIClient()
        user_data = {
            'email': 'user@example.com',
            'password': 'password',
            'name': 'name',
        }
        self.user = create_user(**user_data)
        self.client.force_authenticate(user=self.user)

    def test_obtain_my_info(self):
        """Test for retrieve logged user's info"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': 'user@example.com',
            'name': 'name',
        })

    def test_post_me_not_allowed(self):
        """Check that its not allowed to post in me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_user_info(self):
        """Test for retrieve logged user's info"""
        payload = {
                    'email': 'newuser@example.com',
                    'password': 'newpassword',
                    'name': 'newname',
                }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
