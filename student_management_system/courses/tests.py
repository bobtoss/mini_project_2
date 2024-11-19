from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()


class CourseTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacheruser",
            email="teacher@example.com",
            password="password",
            role="teacher"
        )
        response = self.client.post('/api/users/auth/jwt/create/', {
            "username": "teacheruser",
            "email": "teacher@example.com",
            "password": "password"
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.course_data = {
            "name": "Math 101",
            "description": "Basic Math Course",
            "instructor": self.teacher.id
        }

    def test_course_creation(self):
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', response.data)

    def test_course_list(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
