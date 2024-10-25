"""
Django settings for piekarniaApi project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from firebase_admin import initialize_app, credentials

credential_path = 'serviceAccount.json'
cred = credentials.Certificate(credential_path)
FIREBASE_APP = initialize_app(cred)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&#$@!)wj5$s!4zzyh8b$eptb-4^n_m!i0k#!w#l6rd1d4jxl%&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'catalog',
    'order',
    'places',
    'cms',
    'rest_framework',
    'fcm_django',
    'corsheaders',
    'authentication',
    'social_django',
    'simple_history',
    'apps.home',
    'crispy_forms'
]

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAze0JW2g:APA91bFeeXAESr8rAyWtvXjMEwPtkffWdo_IY2noOCFdZl_5YHHbIMs2u_xEkHGsG10WX9NyRCNq67OLnV1Ks0jt-r3vr1i_6BgguVBtUE1a1v3hG_SBDgs4N179EeEIQMzt41N64h67",
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware'
]

ROOT_URLCONF = 'piekarniaApi.urls'

CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(CORE_DIR, 'apps/templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', TEMPLATE_DIR]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',  # ?
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
            'libraries': {
                'to_and': 'apps.templates.templatetags.to_and',

            }
        },
    },
]

WSGI_APPLICATION = 'piekarniaApi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'dev_piekarnia_api'),
        'USER': os.environ.get('DB_USER', 'dev_piekarnia_api'),
        'PASSWORD': os.environ.get('DB_PASS', 'Piekarnia#123'),
        'HOST': os.environ.get('DB_HOST', 'host.notbug.pl'),
        'PORT': os.environ.get('DB_PORT', '5432'),
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
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'authentication.passwordValidators.ComplexPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pl-PL'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

TIME_INPUT_FORMATS = ['%H:%M']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = os.environ.get('SMTP_HOST', 'smtp.mailtrap.io')
EMAIL_HOST_USER = os.environ.get('SMTP_USER', '84afd23d9f1cd1')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASS', '37babbd282a7f2')
EMAIL_PORT = os.environ.get('SMTP_PORT', '2525')
EMAIL_FROM = os.environ.get('SMTP_FROM', 'no-reply@piekarnia.pl')
EMAIL_TO = os.environ.get('SMTP_TO', 'kontakt@piekarnia.pl')

APP_NAME = os.environ.get('APP_NAME', 'piekarnia')
APP_URL = os.environ.get('APP_URL', 'http://localhost:8000/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 9999,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=72),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = ('127.0.0.1', 'localhost', '0.0.0.0', 'host.notbug.pl')
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://0.0.0.0:4200",
    "http://127.0.0.1:8000"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'sessionId',
    'accept-language',
    'authheaders'
]

CORS_ALLOW_CREDENTIALS = True

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

# LOGIN_URL = 'login'
# LOGOUT_URL = 'logout'
# LOGIN_REDIRECT_URL = 'home'

SOCIAL_AUTH_FACEBOOK_KEY = '1647718275596127'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'd0a65c26a07a48d8a00248d3086551e2'  # App Secret

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # uni_form, bootstrap4

CLIENT_ID = 'mobile_bakery'
CLIENT_SECRET = 'D5SPnhD6hfwE9X74ZoBe'

DOTYKACKA_AUTH_URL = f'https://admin.dotykacka.cz/client/connect?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&scope=*&redirect_uri={APP_URL}/places/list&state='
DOTYKACKA_GET_ACCESS_TOKEN_URL = 'https://api.dotykacka.cz/v2/signin/token'
DOTYKACKA_URL = 'https://api.dotykacka.cz/v2/clouds/'
