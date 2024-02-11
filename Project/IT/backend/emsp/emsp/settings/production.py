from .base import *  # noqa

ALLOWED_HOSTS = [
    'alirezaazadi.com',
]

DEBUG = False

CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS', default='').split(',')
