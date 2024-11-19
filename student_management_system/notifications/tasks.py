from celery import shared_task
from django.core.mail import send_mail
from students.models import Student
from grades.models import Grade
from courses.models import Course
from django.utils import timezone


@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(subject, message, 'admin@example.com', recipient_list)
    return "Email sent successfully!"


@shared_task
def send_daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            subject="Daily Attendance Reminder",
            message="Please remember to mark your attendance today.",
            from_email="admin@example.com",
            recipient_list=[student.user.email]
        )
    return "Daily attendance reminder emails sent."


@shared_task
def send_grade_update_notification(student_id, course_name, grade):
    student = Student.objects.get(pk=student_id)
    send_mail(
        subject="Grade Update Notification",
        message=f"Your grade for {course_name} has been updated to {grade}.",
        from_email="admin@example.com",
        recipient_list=[student.user.email]
    )
    return f"Grade update notification sent to {student.user.email}."


@shared_task
def send_weekly_performance_summary():
    students = Student.objects.all()
    for student in students:
        grades = Grade.objects.filter(student=student)
        attendance_summary = f"Grades: {', '.join([f'{grade.course.name}: {grade.grade}' for grade in grades])}"

        send_mail(
            subject="Weekly Performance Summary",
            message=f"Here is your weekly performance summary:\n{attendance_summary}",
            from_email="admin@example.com",
            recipient_list=[student.user.email]
        )
    return "Weekly performance summary emails sent."
