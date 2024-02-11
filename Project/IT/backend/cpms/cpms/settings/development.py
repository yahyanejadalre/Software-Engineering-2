from datetime import timedelta

from .base import *  # noqa

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

# Django Debug Toolbar must be before any other middleware


MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware', )

# For django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3650),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=36500),
}
