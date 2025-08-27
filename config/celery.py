import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'schedule-habit-notifications-daily': {
        'task': 'habits.tasks.schedule_habit_notifications',
        'schedule': crontab(hour=0, minute=0),
    },
}
