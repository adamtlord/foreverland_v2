from .base import *

# dev overrides
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = True
IS_DEV = True

COMPRESS = False

DOMAIN_NAME = 'localhost:8000'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

STATIC_URL = '/static/'
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
        'NAME': '%s' % PROJECT_NAME,
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        }
    }
}


try:
    from local import *
except ImportError:
    pass
