from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')

app = Celery('StudentManagementSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily-attendance-reminder': {
        'task': 'notifications.tasks.send_daily_attendance_reminder',
        'schedule': crontab(hour=8, minute=0),
    },
    'weekly-performance-summary': {
        'task': 'notifications.tasks.send_weekly_performance_summary',
        'schedule': crontab(weekday=1, hour=9, minute=0),
    },
}
