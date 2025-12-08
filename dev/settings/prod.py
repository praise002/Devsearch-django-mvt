from .base import *

DEBUG = False

ADMINS = [
    ("Praise Idowu", "ifeoluwapraise02@gmail.com"),
]


ALLOWED_HOSTS = ["*"]
DATABASE_URL = config("DATABASE_URL")

DATABASES = {}

if DATABASE_URL:
    import dj_database_url

    if DATABASE_URL.startswith("postgres://"):
        DATABASES["default"] = dj_database_url.config(
            conn_max_age=500,
            conn_health_checks=True,
        )

# REDIS_URL = "redis://cache:6379/0"
REDIS_URL = config("REDIS_URL")  #  prod uses prod redis url

CACHES["default"]["LOCATION"] = REDIS_URL

# CELERY_BROKER_URL = "redis://cache:6379/1"
CELERY_BROKER_URL = config("REDIS_URL")

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)  # Fixed too many redirects
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
