from __future__ import absolute_import, unicode_literals

import os

import dotenv
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyAssistantProject.settings')
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.read_dotenv(env_file)
app = Celery('itvdn')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
