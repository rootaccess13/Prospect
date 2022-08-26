

import os
from pathlib import Path
import django_heroku

from .test import COMPRESS_ROOT, MEDIA_ROOT, STATIC_ROOT
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-63*=$rn1*&9*z!cmn0=t-0jiy-q!n9dz3!o@tiv+t3g^j6#2$q'

DEBUG = True
ALLOWED_HOSTS = ['amateurprospect.herokuapp.com', '127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index.apps.IndexConfig',
    'api.apps.ApiConfig',
    'accounts.apps.AccountsConfig',
    'compressor',
    'hitcount'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
AUTH_USER_MODEL = 'accounts.CustomUser'
ROOT_URLCONF = 'AmateurPlayer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'AmateurPlayer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

DEBUG_PROPAGATE_EXCEPTIONS = False

LOGIN_URL = '/'
CSRF_TRUSTED_ORIGINS = [
    "http://0.0.0.0",
    "http://localhost",
    "http://127.0.0.1",
    "https://amateurprospect.herokuapp.com",
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
COMPRESS_ROOT = os.path.join(BASE_DIR, 'staticfiles')
COMPRESS_URL = '/static/'
COMPRESS_ENABLED = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tena.m.bsinfotech@gmail.com'
EMAIL_HOST_PASSWORD = 'lwegzcmioztymzfc'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_ACCESS_KEY_ID = "AKIATUTGCKKNBNBEEVX5"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "prospectassets"
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_LOCATION = 'static'
AWS_MEDIA = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'AmateurPlayer.storage_backends.MediaStorage'

django_heroku.settings(locals())
CORS_ORIGIN_ALLOW_ALL = True
