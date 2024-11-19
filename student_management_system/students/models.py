from django.db import models
from users.models import User


# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['registration_date']  # Default ordering by registration_date

    def __str__(self):
        return self.user.__str__()