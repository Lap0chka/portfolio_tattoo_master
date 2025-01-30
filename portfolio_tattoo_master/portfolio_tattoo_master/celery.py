import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_tattoo_master.settings')

app = Celery('portfolio_tattoo_master')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()