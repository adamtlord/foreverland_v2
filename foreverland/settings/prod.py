from .base import *

IS_PROD = True

DOMAIN_NAME = 'stage.foreverland.com'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME

ALLOWED_HOSTS = [
    'foreverland.com',
    '.foreverland.com',
    'www.foreverland.com',
]
SSH_HOSTS = 'adamlord.webfactional.com'
STATIC_URL = '%sstatic/' % WWW_ROOT
STATIC_ROOT = '/home/adamlord/webapps/foreverland_staticserve'
MEDIA_URL = '%suploads/' % WWW_ROOT
MEDIA_ROOT = '/home/adamlord/webapps/foreverland_uploadsserve'
STATICFILES_DIRS = [
    '/home/adamlord/webapps/foreverland_django/foreverland/static'
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT

COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'foreverland_mysql',
        'HOST': 'localhost',
        'USER': 'adamlord_fl',
        'PASSWORD': 'IiT77j58tR7yUoKO',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
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
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'foreverland'
EMAIL_HOST_PASSWORD = 'Bubbles14'
SERVER_EMAIL = 'no-reply@foreverland.com'
