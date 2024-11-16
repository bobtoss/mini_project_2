from django.contrib import admin
from .models import Attendance


# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'date', 'status')
    search_fields = ('student__user__username', 'course__name')
    list_filter = ('date', 'status')
