from django.contrib import admin
from .models import Course, Enrollment


# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'instructor')
    search_fields = ('name', 'instructor__username')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'enrollment_date')
    search_fields = ('student__user__username', 'course__name')
