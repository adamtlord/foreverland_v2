from settings.common import *

# prod overrides
DEBUG = False
IS_PROD = True

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
TLD_NAME = DOMAIN_NAME = 'foreverland.com'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = [
    'TLD_NAME',
    '.foreverland.com',
    '.foreverland.com.',
]
DEFAULT_FROM_EMAIL = 'no-reply@%s' % TLD_NAME
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'foreverland'
EMAIL_HOST_PASSWORD = 'Bubbles14'
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SSH_HOSTS = 'adamlord.webfactional.com'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foreverland_db',
        'HOST': 'localhost',
        'USER': 'adamlord_fl',
        'PASSWORD': 'IiT77j58tR7yUoKO',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
        }
    }
}

COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
