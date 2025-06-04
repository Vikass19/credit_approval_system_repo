import os
from celery import Celery

# Make sure this matches your project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')

app = Celery('credit_approval_system')  # This should also match your project name
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
