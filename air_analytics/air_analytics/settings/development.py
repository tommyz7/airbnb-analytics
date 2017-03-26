from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Celery settings
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'django-db'
