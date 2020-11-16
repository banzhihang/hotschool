from __future__ import absolute_import, unicode_literals

import os


from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotSchool.settings')  # 替换 HttpRestServer 为你Django项目的名称

app = Celery('HotSchool')# 替换 HttpRestServer 为你Django项目的名称
platforms.C_FORCE_ROOT = True
app.conf.task_default_queue = 'app'    # 默认队列名称为Celery
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 定时任务
app.conf.beat_schedule = {
    'clear_question': {
        'task': 'question.tasks.check_hot_question_expire_time',
        'schedule': crontab(minute=20,hour=0),
    }
}

if __name__ == '__main__':
    app.start()
