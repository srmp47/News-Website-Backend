import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsWebsiteBackend.settings')
app = Celery('NewsWebsiteBackend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()