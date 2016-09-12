import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WSGI_APPLICATION = 'foreverland.wsgi.application'
PROJECT_NAME = 'foreverland'
ADMINS = (
    ('Alerts', 'adam@foreverland.com'),
)
TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
SECRET_KEY = 'awozw7pth$35zwy%*yx3!2uuna-1(^rr9u(iha0-0ruvy^i@)z'
DEFAULT_CHARSET = 'utf-8'
ROOT_URLCONF = 'urls'

STATIC_URL = '/static/'
STATIC_ROOT = '/home/adamlord/webapps/foreverland_static_v2/'
MEDIA_URL = '/uploads/'
MEDIA_ROOT = '/home/adamlord/webapps/foreverland_uploads_v2/'

DEBUG = False
IS_DEV = False
IS_STAGING = False
IS_PROD = False

ENV = os.getenv('ENV')
if not ENV:
    raise Exception('Environment variable ENV is required!')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

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

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.csrf',
                'django.core.context_processors.debug',
                'django.core.context_processors.media',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',

                'django_common.context_processors.common_settings',

                'apps.common.context_processors.random_quote',
                'apps.common.context_processors.list_years_with_gigs',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_extensions',

    'registration',
    'compressor',
    'django_common',
    'sorl.thumbnail',

    'marketing',
    'members',
    'shows',
    'songs',
    'media',
    'accounts',
    'common',
    'legacy',
    'fidouche',
    'setter',
]

# auth / django-registration params
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/accounts/login/error/'
SEND_EMAIL_AFTER_REGISTRATION = False  # default: False
SEND_EMAIL_AFTER_ACTIVATION = True  # default: True
AUTOMATIC_ACTIVATION_AFTER_REGISTRATION = True  # default: True

AUTHENTICATION_BACKENDS = [
    'django_common.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

GOOGLE_MAPS_API_KEY = 'AIzaSyDf0TeojAvLH_Xne55O7jcVtTfusoIhkrs'

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'PASSWORD': '', 'USER': ''}

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]


# helper function to extend all the common lists
def extend_list_avoid_repeats(list_to_extend, extend_with):
    """Extends the first list with the elements in the second one, making sure its elements are not already there in the
    original list."""
    list_to_extend.extend(filter(lambda x: not list_to_extend.count(x), extend_with))
