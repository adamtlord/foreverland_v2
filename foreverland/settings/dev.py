from .base import *

# dev overrides
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True
IS_DEV = True

COMPRESS = False

DOMAIN_NAME = 'localhost:8000'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

SITE_ID = 1

STATIC_URL = '/static/'
STATIC_ROOT = '{}/staticserve'.format(PROJECT_ROOT)
STATICFILES_DIRS = [
    '{}/static'.format(PROJECT_ROOT),
]
MEDIA_URL = '/uploads/'
MEDIA_ROOT = '{}/uploads'.format(PROJECT_ROOT)
# other
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

extend_list_avoid_repeats(INSTALLED_APPS, [
    'django_extensions'
])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foreverland',
        'HOST': 'db',
        'USER': 'mysql',
        'PASSWORD': 'abc123',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        }
    }
}

INTERNAL_IPS = ['127.0.0.1']
try:
    from local import *
except ImportError:
    pass
