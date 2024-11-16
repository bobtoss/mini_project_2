from django.db import models
from students.models import Student
from courses.models import Course


# Create your models here.
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.BooleanField()

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        status = "Present" if self.status else "Absent"
        return f"{self.student.__str__()} - {self.course.__str__()}: {status} on {self.date}"