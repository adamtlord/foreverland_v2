from settings.common import *

ALLOWED_HOSTS = [
    'foreverland.com',
    '.foreverland.com',
    'www.foreverland.com',
]

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
