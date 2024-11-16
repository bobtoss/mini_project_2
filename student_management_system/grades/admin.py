from django.contrib import admin
from .models import Grade


# Register your models here.

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'grade', 'date', 'teacher')
    search_fields = ('student__user__username', 'course__name', 'teacher__username')
