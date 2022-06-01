import django_heroku
import os
import psycopg2
import dj_database_url
import sys
from decouple import config, Csv
from corsheaders.defaults import default_headers

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*1024

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

HMP_CHECK_TIME = config("HMP_CHECK_TIME")

DEBUG = config("DEBUG",cast=bool)

ITEM_NAME_TH = config("ITEM_NAME_TH")
ITEM_DESCRIPTION_TH = config("ITEM_DESCRIPTION_TH")

ACCESS_TOKEN_EXPIRATION = config('ACCESS_TOKEN_EXPIRATION', cast=int)

SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

AUTH_CLIENT_ID = config('AUTH_CLIENT_ID', cast=Csv())
AUTH_REDIRECT_URLS = config('AUTH_REDIRECT_URLS', cast=Csv())

DEBUG_PROPAGATE_EXCEPTIONS = config('DEBUG_PROPAGATE_EXCEPTIONS', cast=bool)

# BUILD_VERSION = "msnmatch-alpha-0.206"

CURRENT_YEAR = config('CURRENT_YEAR', cast=int)
CURRENT_SEMESTER = config('CURRENT_SEMESTER')

# Applications

INSTALLED_APPS = [
    'channels',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'social_django',
    'users',
    'courses',
    'friendship',
    'storages',
    'skills',
    'webpack_loader',
    'comments',
    'market',
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

ASGI_APPLICATION = 'msnmatch.asgi.application'

WSGI_APPLICATION = 'msnmatch.wsgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
            # "hosts": [('mango-student-matching', 6379)],
            # "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT"),
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.microsoft.MicrosoftOAuth2',
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
)

USER_FIELDS = ["first_name", "last_name", "username", "email"]

SOCIAL_AUTH_MICROSOFT_GRAPH_KEY = config('SOCIAL_AUTH_MICROSOFT_GRAPH_KEY')
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET = config('SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_URL_NAMESPACE = config('SOCIAL_AUTH_URL_NAMESPACE')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = config('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS', cast=Csv())
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = config('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS', cast=Csv())

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = ''


# Password validation

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%m/%d/%Y']

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Access-Control-Allow-Origin',
]
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
CORS_ALLOW_CREDENTIALS = True

AWS_DEFAULT_ACL = "public-read"

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
