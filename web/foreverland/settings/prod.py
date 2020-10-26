import os
from .base import *

IS_PROD = True
DEBUG = False
DOMAIN_NAME = 'foreverland.com'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME

ALLOWED_HOSTS = [
    'foreverland.com',
    '.foreverland.com',
    'www.foreverland.com',
]
ADMINS = ['adam@foreverland.com']

# SSH_HOSTS = 'adamlord.webfactional.com'
STATIC_URL = '%sstatic/' % WWW_ROOT
# STATIC_ROOT = '/home/adamlord/webapps/foreverland_staticserve'
STATIC_ROOT = STATIC_URL
MEDIA_URL = '%suploads/' % WWW_ROOT
MEDIA_ROOT = MEDIA_URL
# MEDIA_ROOT = '/home/adamlord/webapps/foreverland_uploadsserve'
# STATICFILES_DIRS = [
#     '/home/adamlord/webapps/foreverland_django/foreverland/static'
# ]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OUTPUT_DIR = ''
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]


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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/adamlord/memcached.sock',
    }
}

ADMINS = (
    ('Alerts', 'adam@foreverland.com'),
)
# EMAIL_HOST = 'smtp.webfaction.com'
# EMAIL_HOST_USER = 'foreverland'
# EMAIL_HOST_PASSWORD = 'Bubbles14'
# SERVER_EMAIL = 'no-reply@foreverland.com'
# DEFAULT_FROM_EMAIL = SERVER_EMAIL
