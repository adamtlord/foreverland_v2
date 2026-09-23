import os

from .base import *  # noqa: F401 F403
from .env import env_bool

DEBUG = env_bool("DEBUG", "0")
IS_PROD = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

DOMAIN_NAME = "foreverland.com"
WWW_ROOT = "https://%s/" % DOMAIN_NAME

STATIC_ROOT = "/home/ubuntu/app/staticfiles"
MEDIA_ROOT = "/home/ubuntu/app/mediafiles"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = [
    "https://foreverland.com",
    "https://www.foreverland.com",
]

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587") or 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", "1")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "noreply@foreverland.com"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "%s" % os.getenv("MYSQL_DATABASE"),
        "HOST": "%s" % os.getenv("MYSQL_HOST"),
        "USER": "%s" % os.getenv("MYSQL_USER"),
        "PASSWORD": "%s" % os.getenv("MYSQL_PASSWORD"),
        "OPTIONS": {
            "init_command": "SET default_storage_engine=INNODB",
        },
    }
}
