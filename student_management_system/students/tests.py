from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class StudentTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="password",
            role="admin"
        )
        response = self.client.post('/api/users/auth/jwt/create/', {
            "username": "adminuser",
            "email": "admin@example.com",
            "password": "password"
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_student_creation(self):
        new_user = User.objects.create_user(
            username="newstudent",
            email="newstudent@example.com",
            password="newpassword"
        )
        student_data = {"user": new_user.id, "dob": "1995-05-05"}
        response = self.client.post('/api/students/', student_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('dob', response.data)

    def test_student_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
