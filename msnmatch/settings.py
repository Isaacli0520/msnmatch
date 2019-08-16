"""
Django settings for msnmatch project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import django_heroku
import os
import psycopg2
import dj_database_url
import sys
from decouple import config, Csv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f@hcb!l&kpn_4u+iz)6j4w(5j4$b2!)-=*j(9&(x_0a-j8o6)5'

DEBUG = config("DEBUG",cast=bool)

SECURE_SSL_REDIRECT = not DEBUG
# SESSION_COOKIE_SECURE = not DEBUG
# CSRF_COOKIE_SECURE = not DEBUG

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DEBUG_PROPAGATE_EXCEPTIONS = config('DEBUG_PROPAGATE_EXCEPTIONS', cast=bool)

BUILD_VERSION = "msnmatch-alpha-0.206"

CURRENT_YEAR = config('CURRENT_YEAR', cast=int)
CURRENT_SEMESTER = config('CURRENT_SEMESTER')

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'social_django',
    'users',
    'courses',
    'widget_tweaks',
    'friendship',
    'storages',
    'skills',
    'webpack_loader',
    'groups',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'msnmatch.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        },
    },
]

WSGI_APPLICATION = 'msnmatch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_URL_NAMESPACE = config('SOCIAL_AUTH_URL_NAMESPACE')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = config('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS', cast=Csv())
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = config('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS', cast=Csv())

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%m/%d/%Y']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST", cast=Csv())
CORS_ALLOW_CREDENTIALS = True

# AWS_DEFAULT_ACL = None

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_CLOUDFRONT_DOMAIN = config('AWS_CLOUDFRONT_DOMAIN')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000',
}

AWS_LOCATION = 'static'

# STATIC_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/' + AWS_LOCATION + '/'
# STATIC_URL = 'https://' + AWS_CLOUDFRONT_DOMAIN + '/' + BUILD_VERSION + '/' + AWS_LOCATION + '/'
# STATICFILES_STORAGE = 'msnmatch.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'msnmatch.storage_backends.MediaStorage' 

STATIC_HOST = config('STATIC_HOST') if not DEBUG else ''
# STATIC_HOST = ""
STATIC_URL = STATIC_HOST + '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'src/assets/static'),
    os.path.join(BASE_DIR, 'dist'),
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': '/dist/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

django_heroku.settings(locals(), staticfiles=False)

db_config = dj_database_url.config()
if db_config:
    DATABASES['default'] =  db_config
