from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atp.settings')

app = Celery('atp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Load periodic tasks
app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'sync_azure_vm_sizes_to_db': {
        'task': 'courses.tasks.sync_azure_vm_sizes_to_db',
        'schedule': crontab(minute='0', hour='1'),  # every day at 1am
        'args': ()
    }
}