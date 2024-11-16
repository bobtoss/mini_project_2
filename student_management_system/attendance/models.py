from django.db import models
from student_management_system.students.models import Student
from student_management_system.courses.models import Course


# Create your models here.
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.BooleanField()
