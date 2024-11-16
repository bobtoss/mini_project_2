from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User


# Create your models here.
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    date = models.DateField(auto_now=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.__str__()} - {self.course.__str__()}: {self.grade}"