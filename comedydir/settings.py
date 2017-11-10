"""
Django settings for comedydir project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from os.path import join, dirname
import dj_database_url
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hg%!x5_9fc)-_$$wdm0)+6awb32xe2i454lu&!1v9mcesxeanz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'comedydir-backend.herokuapp.com',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'events.apps.EventsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'mapwidgets',
    'debug_toolbar',
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'comedydir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'comedydir.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
# Gets DB config from DATABASE_URL env variable
DATABASES['default'].update(db_from_env)
DATABASES['default']['ENGINE']= 'django.contrib.gis.db.backends.postgis'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS =[
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# STATIC_ROOT = 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

GOOGLE_MAP_API_KEY = GOOGLE_API_KEY = GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyCfEghEN8EUWO5-w6aEof1vnc5xSFJ0f3U'

MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": GOOGLE_MAP_API_KEY
}

# Do not set on server so they default to NONE
# https://www.alextomkins.com/2017/08/fixing-gdal-geos-django-macos/
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')

INTERNAL_IPS = ['127.0.0.1']


# FB
FACEBOOK_APP_ID = '122406461820685'
FACEBOOK_APP_SECRET = '18690ef187ee39ef6a084f68670d34df'
FACEBOOK_ACCESS_TOKEN = '{}|{}'.format(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
FACEBOOK_GRAPH_API_VERSION = '2.10'
#
# AUTHENTICATION_BACKENDS = (
#     'django_facebook.auth_backends.FacebookBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )
#
# AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'

REST_FRAMEWORK = {
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

FACEBOOK_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

# TODO: Whitelist production domain when it's up
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     'google.com',
#     'hostname.example.com',
#     'localhost:8000',
#     '127.0.0.1:9000'
# )

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')
