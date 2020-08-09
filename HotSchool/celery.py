from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotSchool.settings')  # 替换 HttpRestServer 为你Django项目的名称

app = Celery('HotSchool')# 替换 HttpRestServer 为你Django项目的名称

app.conf.task_default_queue = 'app'    # 默认队列名称为Celery
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# app.conf.update(
#   CELERYBEAT_SCHEDULE = {
#     'send-report': {
#       'task': 'deploy.tasks.report',
#       'schedule': crontab(hour=4, minute=30, day_of_week=1),
#     }
#   }
# )

