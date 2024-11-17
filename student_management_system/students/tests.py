from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class StudentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="studentuser", email="student@example.com", password="password")
        self.client.login(username="studentuser", password="password")
        self.student_data = {
            "user": {
                "username": "studentuser",
                "email": "student@example.com"
            },
            "dob": "2000-01-01"
        }

    def test_student_creation(self):
        response = self.client.post('/api/v1/students/', self.student_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('dob', response.data)

    def test_student_list(self):
        response = self.client.get('/api/v1/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
