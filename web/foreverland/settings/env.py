import os

from django.core.exceptions import ImproperlyConfigured


def env_bool(name, default="0"):
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


def require_secret_key():
    key = os.environ.get("SECRET_KEY")
    if not key:
        raise ImproperlyConfigured("SECRET_KEY is required")
    return key


def require_allowed_hosts():
    hosts = os.environ.get("DJANGO_ALLOWED_HOSTS")
    if not hosts:
        raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS is required")
    return hosts.split()
