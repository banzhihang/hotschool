from celery import Celery
from django.conf import settings
import os

# 为celery设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotSchool.settings')

# 创建应用
app = Celery("demo")
# 配置应用
app.conf.update(
    # 配置broker, 这里我们用redis作为broker broker_url
    broker_url='amqp://guest@localhost//',
    result_backend='django-db',
)
# 设置app自动加载任务
# 从已经安装的app中查找任务
app.autodiscover_tasks(settings.INSTALLED_APPS)