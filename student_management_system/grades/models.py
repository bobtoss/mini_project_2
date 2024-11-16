from django.db import models
from student_management_system.students.models import Student
from student_management_system.courses.models import Course
from student_management_system.users.models import User


# Create your models here.
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    date = models.DateField(auto_now=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
