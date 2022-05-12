"""
Django settings for opal project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import logging
import secrets
from pathlib import Path
import os
import environ

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'vendor')]

env = environ.Env()
if str(BASE_DIR) + "/opal/.env":
    environ.Env.read_env()

# Load environment variables and set defaults
default_secret_key = secrets.token_urlsafe()

ENVIRONMENT = os.getenv("ENVIRONMENT", default="development")
# set SSL active to True if you are using https
SSL_ACTIVE = os.getenv("SSL_ACTIVE", default=False)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("OPAL_SECRET_KEY", default=default_secret_key)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", default="False")
LOG_LEVEL = os.getenv("LOG_LEVEL", default="DEBUG")
# Set proxy servers if needed. This will be used when the app attempts to download catalog files from the internet
HTTP_PROXY = os.getenv("HTTP_PROXY", default=False)
HTTPS_PROXY = os.getenv("HTTPS_PROXY", default=False)
# Database settings
DATABASE = os.getenv("DATABASE", default="sqlite")
DB_NAME = os.getenv("DB_NAME", default="db.sqlite3")
# These can be blank if using sqlite
DB_PASSWORD = os.getenv("DB_PASSWORD", default="")
DB_USER = os.getenv("DB_USER", default="opal")
DB_HOST = os.getenv("DB_HOST", default="localhost")
DB_PORT = os.getenv("DB_PORT", default="5432")
# OIDC settings
ENABLE_OIDC = os.getenv("ENABLE_OIDC", default=False)
OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID", default="")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET", default="")
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv("OIDC_OP_AUTHORIZATION_ENDPOINT", default="")
OIDC_OP_TOKEN_ENDPOINT = os.getenv("OIDC_OP_TOKEN_ENDPOINT", default="")
OIDC_OP_USER_ENDPOINT = os.getenv("OIDC_OP_USER_ENDPOINT", default="")
OIDC_RP_SIGN_ALGO = os.getenv("OIDC_RP_SIGN_ALGO", default="")
OIDC_OP_JWKS_ENDPOINT = os.getenv("OIDC_OP_JWKS_ENDPOINT", default="")
OIDC_OP_LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", default="")
OIDC_OP_LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", default="")
# SAML settings
ENABLE_SAML = os.getenv("ENABLE_SAML", default=False)
SAML_SETTINGS_JSON = os.getenv("SAML_SETTINGS_JSON", default='saml_settings_template.json')
SAML_CSRF_TRUSTED_ORIGINS = os.getenv("SAML_CSRF_TRUSTED_ORIGINS", default="")
SAML_TECHNICAL_POC = os.getenv("SAML_TECHNICAL_POC", default=False)
SAML_TECHNICAL_POC_EMAIL = os.getenv("SAML_TECHNICAL_POC_EMAIL", default=False)
SAML_SUPPORT_POC = os.getenv("SAML_SUPPORT_POC", default=False)
SAML_SUPPORT_POC_EMAIL = os.getenv("SAML_SUPPORT_POC_EMAIL", default=False)
SAML_CERT = os.getenv("SAML_CERT", default="")
SAML_KEY = os.getenv("SAML_KEY", default="")
SAML_FOLDER = os.path.join(BASE_DIR, os.getenv("SAML_FOLDER", default="saml"))

# Handling allowed hosts a little different since we have to turn it into a list.
# If providing a value, you just need to provide a comma separated string of hosts
# You don't need to quote anything or add [] yourself.
if SSL_ACTIVE:
    protocol = "https://"
else:
    protocol = "http://"

if env.__contains__("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(',')
    CSRF_TRUSTED_ORIGINS = []
    for host in ALLOWED_HOSTS:
        CSRF_TRUSTED_ORIGINS.append(protocol + host)
else:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = [protocol + '*.localhost', protocol + '*.127.0.0.1']



# Other Variables
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2048
ROOT_URLCONF = 'opal.urls'
WSGI_APPLICATION = 'opal.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

if ENVIRONMENT == "production":
    SECURE_SSL_REDIRECT = True
else:
    print("Running in Development mode!")
    for k, v in sorted(os.environ.items()):
        print(k + ':', v)

# Application definition

# These are the applications defined in opal and map to OSCAL models.
# We track them separately here because we use this list for some functions
# that have to cycle through all apps
USER_APPS = ['common', 'catalog', 'control_profile', 'component_definition', 'ssp', ]

INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', "bootstrap5",
                  'django_extensions', ]

# Add the user defined applications to INSTALLED_APPS
INSTALLED_APPS.extend(USER_APPS)

if ENVIRONMENT == "development":
    INSTALLED_APPS.extend(['coverage', ])

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware', ]
# To enable sitewide caching
# MIDDLEWARE_FOR_CACHE = ['django.middleware.cache.UpdateCacheMiddleware',
#               'django.middleware.common.CommonMiddleware', 'django.middleware.cache.FetchFromCacheMiddleware',]
# MIDDLEWARE.extend(MIDDLEWARE_FOR_CACHE)

ROOT_URLCONF = 'opal.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.contrib.messages.context_processors.messages', ],
    },
}, ]

# DEFAULT_FILE_STORAGE = 'binary_database_files.storage.DatabaseStorage'

WSGI_APPLICATION = 'opal.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if DATABASE == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': env('DB_NAME'), 'USER': env('DB_USER'),
            'PASSWORD': env('DB_PASSWORD'), 'HOST': env('DB_HOST'), 'PORT': env('DB_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, DB_NAME),
        }
    }

print("using database " + DATABASES['default']['NAME'])

# Adding support for SAML Authentication
if ENABLE_OIDC:
    INSTALLED_APPS.extend(['mozilla_django_oidc', ])
    AUTHENTICATION_BACKENDS = ('mozilla_django_oidc.auth.OIDCAuthenticationBackend',)

if ENABLE_SAML:
    saml_csrf_trusted_origins_list = SAML_CSRF_TRUSTED_ORIGINS.split(',')
    for site in saml_csrf_trusted_origins_list:
        CSRF_TRUSTED_ORIGINS.append(protocol + site)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
}, ]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Logging Information
LOGGING = {
    'version': 1,
    # Version of logging
    'disable_existing_loggers': False,
    # disable logging
    # Formatters ###########################################################
    'formatters': {
        'verbose': {
            'format': '{levelname} : {asctime} : {filename} line {lineno} in function {funcName} : {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    # Handlers #############################################################
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'opal-debug.log',
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose'
        },
    },
    # Filters ####################################################################
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    # Loggers ####################################################################
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': LOG_LEVEL
        },
        'debug': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'werkzeug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}