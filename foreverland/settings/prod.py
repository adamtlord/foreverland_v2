from .base import *

IS_PROD = True

DOMAIN_NAME = 'stage.foreverland.com'
WWW_ROOT = 'http://%s/' % DOMAIN_NAME

ALLOWED_HOSTS = [
    'foreverland.com',
    '.foreverland.com',
    'www.foreverland.com',
]

STATIC_URL = '%s/static/' % WWW_ROOT
STATIC_ROOT = '/home/adamlord/webapps/foreverland_staticserve/'
MEDIA_URL = '%s/uploads/' % WWW_ROOT
MEDIA_ROOT = '/home/adamlord/webapps/foreverland_uploadsserve/'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
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
            'init_command': 'SET storage_engine=INNODB',
        }
    }

}

ADMINS = (
    ('Alerts', 'adam@foreverland.com'),
)
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'foreverland'
EMAIL_HOST_PASSWORD = 'Bubbles14'
SERVER_EMAIL = 'no-reply@foreverland.com'
