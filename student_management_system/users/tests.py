from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        # Authenticate the user and obtain the token
        response = self.client.post('/api/users/auth/jwt/create/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_user_registration(self):
        new_user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "pass123456",
            "re_password": "pass123456"
        }
        response = self.client.post('/api/users/auth/users/', new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)

    def test_user_login(self):
        response = self.client.post('/api/users/auth/jwt/create/', {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
