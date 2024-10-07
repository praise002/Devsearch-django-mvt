from .base import *

DEBUG = False

ADMINS = [
    ('Praise Idowu', 'ifeoluwapraise02@gmail.com'),
]

# ALLOWED_HOSTS = ['.vercel.app'] 
ALLOWED_HOSTS = ['*'] 

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": "db",
        "PORT": config("DB_PORT"),
    }
}

REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }