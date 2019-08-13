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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f@hcb!l&kpn_4u+iz)6j4w(5j4$b2!)-=*j(9&(x_0a-j8o6)5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ALLOWED_HOSTS = ['msn-match-test.herokuapp.com', 'match.msnatuva.org','localhost']
ALLOWED_HOSTS = []

DEBUG_PROPAGATE_EXCEPTIONS = True

BUILD_VERSION = "msnmatch-alpha-0.206"

CURRENT_YEAR = 2020
CURRENT_SEMESTER = "2019Fall"

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
        'NAME': 'msnmatch',
        'USER': 'msn',
        'PASSWORD': 'msnatuva',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '490419116742-ms0u7ogu2ng11drtqofgscvqhmt8o7vu.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'pfR-vOTg6Zhb20TmLds5RgeX'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['virginia.edu']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = ['fz233ubw@gmail.com', 'mango.cs3240@gmail.com']

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


CORS_ORIGIN_WHITELIST = (
    'https://127.0.0.1:8080',
    'http://127.0.0.1:8080',
    'https://localhost:8080', 
    'http://localhost:8080', 
    'https://plannable.gitee.io',
    'http://plannable.gitee.io',
)
CORS_ALLOW_CREDENTIALS = True

# AWS_DEFAULT_ACL = None

AWS_ACCESS_KEY_ID = 'AKIAS2S3QXP6X5BJWVNA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mango-orange'
AWS_CLOUDFRONT_DOMAIN = 'drx0170jym8dn.cloudfront.net'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000',
}


# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
AWS_LOCATION = 'static'

# STATIC_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/' + AWS_LOCATION + '/'
# STATIC_URL = 'https://' + AWS_CLOUDFRONT_DOMAIN + '/' + BUILD_VERSION + '/' + AWS_LOCATION + '/'
# STATICFILES_STORAGE = 'msnmatch.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'msnmatch.storage_backends.MediaStorage' 

STATIC_HOST = 'https://d1ixiphwkdejqh.cloudfront.net' if not DEBUG else ''
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
