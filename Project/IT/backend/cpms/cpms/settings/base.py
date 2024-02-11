"""
Django settings for cpms project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

"""
a) know the location and “external” status of a charging station (number of charging sockets
available, their type such as slow/fast/rapid, their cost, and, if all sockets of a certain type are
occupied, the estimated amount of time until the first socket of that type is freed);
b) start charging a vehicle according to the amount of power supplied by the socket, and monitor
the charging process to infer when the battery is full;c) know the “internal” status of a charging station (amount of energy available in its batteries, if
any, number of vehicles being charged and, for each charging vehicle, amount of power
absorbed and time left to the end of the charge);
d) acquire by the DSOs information about the current price of energy;
e) decide from which DSO to acquire energy (if more than one is available);
f) dynamically decide where to get energy for charging (station battery, DSO, or a mix thereof
according to availability and cost).
"""

import warnings
from pathlib import Path

import environ

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


BASE_DIR = Path(__file__).resolve().parent
env = environ.Env(DEBUG=(bool, False))  # set default values and casting

# Disable warnings if the .env file is not found
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    environ.Env.read_env(BASE_DIR / 'environments' / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.gis',
    'rest_framework_simplejwt',
    'rest_framework',
    'django_filters',

    'app_dso',
    'app_user',
    'app_admin',
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
]

ROOT_URLCONF = 'cpms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
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

WSGI_APPLICATION = 'cpms.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.str('DEFAULT_DB_NAME'),
        'USER': env.str('DEFAULT_DB_USER'),
        'PASSWORD': env.str('DEFAULT_DB_PASSWORD'),
        'HOST': env.str('DEFAULT_DB_HOST'),
        'PORT': env.str('DEFAULT_DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    # 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utilities.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # Due to the externally poor performance of the Browsable API in case of using ViewSets,
        # we are using the JSONRenderer as the default renderer in the production environment.
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

EMSP_API_URL = env.str('EMSP_URL', default='http://localhost:8000/api/')
EMSP_USERNAME = env.str('EMSP_USERNAME', default='emsp')
EMSP_PASSWORD = env.str('EMSP_PASSWORD', default='emsp')
