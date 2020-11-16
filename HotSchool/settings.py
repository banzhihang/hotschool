"""
Django settings for HotSchool project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from datetime import timedelta, datetime
import django_celery_results
import redis

import logging
import django.utils.log
import logging.handlers



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ay41!8_m%x4vzvrxev%)6h6d-#@@1#6@68sy9zzm7i*094-xtd'

# 七牛云设置
QINIU_AK = 'GRtg7K60aDrY4e6LhjHsf-8g4zm3jXCS0IokOvPx'
QINIU_SK = 'AQkS-YUZ7oS0J6mkWx4CN6-ggwTZpdGqm_9MPPev'
QINIU_BUCKET_NAME = 'hotschool'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

log_path = os.path.join(BASE_DIR, "logs")
if not os.path.exists(log_path):
    os.makedirs("logs")


LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        'console': {     # 在终端打印
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'simple'
        },
        'default': {    # 默认的
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_DIR+'/logs/', "all.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,                    # 日志大小 50M
            'backupCount': 3,                                # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {   # 专门用来记错误日志
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_DIR+'/logs/', "error.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'collect': {   # 专门定义一个收集特定信息的日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_DIR+'/logs/', "collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/', "script.log"),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
        }
    },
    'loggers': {
        'django': {             # 默认的logger应用如下配置
            'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        'collect': {      # 名为 'collect'的logger还单独处理
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
    },
}

ALLOWED_HOSTS = ['*']

# drf设置
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES':[
        'rest_framework.renderers.JSONRenderer',
    ],
}

# channel设置
ASGI_APPLICATION = 'HotSchool.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# 跨域设置
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# jwt过期时间
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=10)
}

# celery配置·
CELERY_IGNORE_RESULT = True  # 忽略执行结果
CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'  # 消息队列
CELERY_TASK_SERIALIZER = 'pickle'  # 序列化的数据类型
CELERY_ACCEPT_CONTENT = ['json', 'pickle']  # 接受的数据类型

# Application definition
INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'haystack',
    'rest_framework',
    'user',
    'question',
    'operation',
    'communicate',
    'food',
    'upload',
    'recommend',
    'draft',
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HotSchool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'HotSchool.wsgi.application'


# 数据库相关配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hotschool',
        'USER': 'root',
        'PASSWORD': 'BZH1319552910',
        'HOST': '127.0.0.1'
    }
}
# haystack配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'apps.search.elasticsearch2_ik_backend.Elasticsearch2IkSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
# 搜索引擎设置 当添加、修改、删除数据时，自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# Django的缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# redis连接池
POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1, decode_responses=True)

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# 推荐数量
RECOMMENT_NUMBER = 8

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# 匿名头像url
ANONYMITY_USER_HEAD_IMAGE = 'https://qiniu.ifelse.top/20201013165636583.png'

# 静态文件路径
STATIC_ROOT = os.path.join(BASE_DIR, "static")
