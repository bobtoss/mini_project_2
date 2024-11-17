from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "re_password": "testpassword"
        }

    def test_user_registration(self):
        response = self.client.post('/api/v1/auth/users/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)

    def test_user_login(self):
        # Register user first
        self.client.post('/api/v1/auth/users/', self.user_data)
        response = self.client.post('/api/v1/auth/token/login/', {
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
