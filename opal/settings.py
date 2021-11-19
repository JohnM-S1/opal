"""
Django settings for opal project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from opal.local_settings import env

#Path variables for application
BASE_DIR = str(Path(__file__).resolve(strict=True).parent.parent)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
IMPORTED_CATALOGS_DIR = 'catalogs/'

# Other Variables
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2048
ROOT_URLCONF = 'opal.urls'
WSGI_APPLICATION = 'opal.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#Set reasonable defaults for environment values
env_defaults = {
    "env" : "development",
    "opal_secret_key" : "=am5inf!4e36^9xwzt3r5$j#kv@g%9c@yya5xa-8&6v!1_bvq!",
    "debug" : "True",
    "allowed_hosts" : ["*"],
    "database" : "sqlite",
    "db_password" : "",
    "db_name" : "",
    "db_user" : "",
    "db_host" : "localhost",
    "db_port" : "",
    "adfs_enabled" : False,
    "adfs_server" : "adfs.server.url",
    "adfs_client_id" : "3fbddfb7-bb0a-4eb8-9b8d-756a52e4e6b7",
    "adfs_client_id" : "00000000-0000-0000-0000-000000000000",
    "adfs_relying_party_id" : "00000000-0000-0000-0000-000000000000",
    "adfs_audience" : "microsoft:identityserver:00000000-0000-0000-0000-000000000000",
}

if os.path.exists(os.path.join(BASE_DIR,'opal','local_settings.py')):
    from opal.local_settings import env
else:
    env = {}

for k in env_defaults:
    if k not in env:
        env[k] = env_defaults[k]
        #print("No value found for variable ",k," using default value of " + str(env_defaults[k]))
    # else:
        # print("Value found for variable ",k," (",str(env[k]),")")

if env["env"] == "development":
    print("Running in Development mode!")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env["opal_secret_key"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env["debug"]
ALLOWED_HOSTS = env["allowed_hosts"]


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'dal_queryset_sequence',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'django_extensions',
    'fixture_magic',
    'rest_framework',
    'rest_framework_tricks',
    'ssp.apps.ssp',
    'coverage',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.contrib.staticfiles',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ssp/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if env["database"] == "sqlite":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR + '/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env['db_name'],
            'USER': env['db_user'],
            'PASSWORD': env["db_password"],
            'HOST': env["db_host"],
            'PORT': env["db_port"],
        }
    }

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        # If you're performance testing, you will want to use the browseable API
        # without forms, as the forms can generate their own queries.
        # If performance testing, enable:
        # 'example.utils.BrowsableAPIRendererWithoutForms',
        # Otherwise, to play around with the browseable API, enable:
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_json_api.filters.QueryParameterValidationFilter',
        'rest_framework_json_api.filters.OrderingFilter',
        'rest_framework_json_api.django_filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'SEARCH_PARAM': 'filter[search]',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

if env["adfs_enabled"] :
    INSTALLED_APPS.append('django_auth_adfs')

    # With this you can force a user to login without using
    # the LoginRequiredMixin on every view class
    #
    # You can specify URLs for which login is not enforced by
    # specifying them in the LOGIN_EXEMPT_URLS setting.
    MIDDLEWARE.append('django_auth_adfs.middleware.LoginRequiredMiddleware',)

    AUTHENTICATION_BACKENDS = (
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    )

    # checkout the documentation of django_auth_adfs for more settings
    AUTH_ADFS = {
        "SERVER": env["adfs_server"],
        "CLIENT_ID": env["adfs_client_id"],
        "RELYING_PARTY_ID": env["adfs_relying_party_id"],
        # Make sure to read the documentation about the AUDIENCE setting
        # when you configured the identifier as a URL!
        "AUDIENCE": env["adfs_audience"],
        # "CA_BUNDLE": "/path/to/ca-bundle.pem",
        "CLAIM_MAPPING": {"first_name": "given_name",
                        "last_name": "family_name",
                        "email": "email"},
        "USERNAME_CLAIM": "upn",
        "GROUP_CLAIM": "group"
        }

    # Configure django to redirect users to the right URL for login
    LOGIN_URL = "django_auth_adfs:login"
    LOGIN_REDIRECT_URL = "/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'debug.log')
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file','console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
