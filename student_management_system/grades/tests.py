from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from students.models import Student
from courses.models import Course
from .models import Grade

User = get_user_model()


class GradeTests(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="password",
            role="teacher"
        )
        response = self.client.post('/api/users/auth/jwt/create/', {
            "username": "teacher",
            "email": "teacher@example.com",
            "password": "password"
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.student_user = User.objects.create_user(username="student", email="student@example.com",
                                                     password="password")
        self.student = Student.objects.create(user=self.student_user, dob="2000-01-01")
        self.course = Course.objects.create(name="Science 101", description="Science Course", instructor=self.teacher)
        self.client.login(username="teacher", password="password")
        self.grade_data = {
            "student": self.student.id,
            "course": self.course.id,
            "grade": "A",
            "teacher": self.teacher.id,
        }

    def test_grade_assignment(self):
        response = self.client.post('/api/grades/', self.grade_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('grade', response.data)

    def test_grade_list(self):
        response = self.client.get('/api/grades/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
