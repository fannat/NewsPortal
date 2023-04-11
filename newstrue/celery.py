import datetime
import os
from celery import Celery
from celery.schedules import crontab
from .settings import INSTALLED_APPS
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newstrue.settings')

app = Celery('newstrue')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_every_monday_8am': {
        'task': 'newstrueapp.tasks.week_post',
        'schedule': crontab(day_of_week=3, hour=22, minute=12),
    },
}