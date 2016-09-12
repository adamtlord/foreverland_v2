from .base import *

# dev overrides
DEBUG = True
IS_DEV = True

COMPRESS = False

DOMAIN_NAME = 'localhost:8000'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# other
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEMPLATE_DEBUG = True

extend_list_avoid_repeats(INSTALLED_APPS, [
    'django_extensions'
])

try:
    from local import *
except ImportError:
    pass
