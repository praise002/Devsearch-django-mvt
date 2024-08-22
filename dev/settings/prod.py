from .base import *

DEBUG = False

ADMINS = [
    ('Praise Idowu', 'ifeoluwapraise02@gmail.com'),
]

ALLOWED_HOSTS = ['.vercel.app'] 

# DATABASES = {
#     'default': {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("POSTGRES_DB"),
#         "USER": config("POSTGRES_USER"),
#         "PASSWORD": config("POSTGRES_PASSWORD"),
#         "HOST": config("POSTGRES_HOST"),
#         "PORT": config("POSTGRES_PORT"),
#     }
# }

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }