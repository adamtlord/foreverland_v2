import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_NAME = "foreverland"
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
WSGI_APPLICATION = "foreverland.wsgi.application"

TIME_ZONE = "America/Los_Angeles"
USE_TZ = False
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True
DEFAULT_CHARSET = "utf-8"
ROOT_URLCONF = "foreverland.urls"

IS_DEV = False
IS_STAGING = False
IS_PROD = False

SITE_ID = 1

COMPRESS_ENABLED = False

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ENV = os.getenv("ENV")
if not ENV:
    raise Exception("Environment variable ENV is required!")

ROOT_URLCONF = "foreverland.urls"

DATABASES = {}

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT + "/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.csrf",
                "django.template.context_processors.debug",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                # 'django_common.context_processors.common_settings',
                "common.context_processors.random_quote",
                "common.context_processors.list_years_with_gigs",
            ],
        },
    },
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.humanize",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django_extensions",
    # 'django_registration',
    "compressor",
    # 'django_common',
    "sorl.thumbnail",
    "marketing",
    "members",
    "shows",
    "songs",
    "media",
    "accounts",
    "common",
    "fidouche",
    "setter",
]

# auth / django-registration params
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = "/accounts/login/error/"
SEND_EMAIL_AFTER_REGISTRATION = False  # default: False
SEND_EMAIL_AFTER_ACTIVATION = True  # default: True
AUTOMATIC_ACTIVATION_AFTER_REGISTRATION = True  # default: True

AUTHENTICATION_BACKENDS = [
    # 'django_common.auth_backends.EmailBackend',
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PROFILE_MODULE = "accounts.UserProfile"

if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "PASSWORD": "",
        "USER": "",
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
GOOGLE_MAPS_API_KEY = "%s" % os.getenv("GOOGLE_MAPS_API_KEY")


# helper function to extend all the common lists
def extend_list_avoid_repeats(list_to_extend, extend_with):
    """Extends the first list with the elements in the second one, making sure its elements are not already there in the
    original list."""
    list_to_extend.extend(filter(lambda x: not list_to_extend.count(x), extend_with))
