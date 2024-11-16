from django.db import models
from student_management_system.users.models import User


# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)
