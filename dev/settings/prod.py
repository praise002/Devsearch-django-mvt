from .base import *

DEBUG = False

ADMINS = [
    ('Praise Idowu', 'ifeoluwapraise02@gmail.com'),
]

# ALLOWED_HOSTS = ['.vercel.app', '.now.sh'] 
ALLOWED_HOSTS = ['*'] 

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": config("POSTGRES_PORT"),
    }
}

REDIS_URL = 'redis://cache:6379/0'
CACHES['default']['LOCATION'] = REDIS_URL

# CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_BROKER_URL = 'redis://cache:6379/1'

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }