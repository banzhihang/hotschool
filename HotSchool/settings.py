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
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import redis

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
# 域名
domain_name = 'http://127.0.0.1:8000'

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK = {
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

# jwt过期时间
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=1000)
}

# celery配置·
CELERY_IGNORE_RESULT = True # 忽略执行结果
CELERY_TIMEZONE = 'Asia/Shanghai' # 时区
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//' # 消息队列
CELERY_TASK_SERIALIZER = 'pickle' # 序列化的数据类型
CELERY_ACCEPT_CONTENT = ['json','pickle'] # 接受的数据类型


# Application definition
INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'haystack',
    'rest_framework',
    'django_celery_beat',
    'user',
    'question',
    'operation',
    'communicate',
    'food',
    'upload',
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
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

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://192.168.31.202:9200/',
        'INDEX_NAME': 'haystack',
    },
}
# 当添加、修改、删除数据时，自动更新索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

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


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=1,decode_responses=True)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
