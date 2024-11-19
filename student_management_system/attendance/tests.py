from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from students.models import Student
from courses.models import Course
from .models import Attendance

User = get_user_model()


class AttendanceTests(APITestCase):

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
        self.course = Course.objects.create(name="History 101", description="History Course", instructor=self.teacher)
        self.client.login(username="teacher", password="password")
        self.attendance_data = {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-11-01",
            "status": True,
        }

    def test_mark_attendance(self):
        response = self.client.post('/api/attendance/', self.attendance_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('status', response.data)

    def test_attendance_list(self):
        response = self.client.get('/api/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
