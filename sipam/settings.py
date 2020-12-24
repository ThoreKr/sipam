"""
Django settings for sipam project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import warnings
from datetime import timedelta
from django.core.cache import CacheKeyWarning
import environ


from .config import SIPAMConfig

try:
    config = environ.to_config(SIPAMConfig)
except environ.exceptions.MissingEnvValueError as e:
    print(f"Missing Key: {e}")
    print(SIPAMConfig.generate_help(display_defaults=True))
    exit(1)


# ignore cache key warning from drf-oidc-provider
warnings.simplefilter("ignore", CacheKeyWarning)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.secret_key

# This sets the key of the claim which defines the array of groups the user is in.

OIDC_GROUPS_CLAIM = config.oidc.groups_claim


def allowed_groups() -> dict:
    if config.oidc.groups_claim:
        return {
            f'{config.oidc.groups_claim}': {
                'values': config.oidc.allowed_groups,
                'essential': True
            }
        }
    return {}


# OIDC configuration drf-oidc-auth
OIDC_AUTH = {
    # Specify OpenID Connect endpoint. Configuration will be
    # automatically done based on the discovery document found
    # at <endpoint>/.well-known/openid-configuration
    'OIDC_ENDPOINT': config.oidc.endpoint,

    'OIDC_CLAIMS_OPTIONS': {
        'azp': {
            'values': [
                "{config.oidc.client_id}",
            ],
            'essential': True,
        },
        **allowed_groups(),
    },
    # (Optional) Function that resolves id_token into user.
    # This function receives a request and an id_token dict and expects to
    # return a User object. The default implementation tries to find the user
    # based on username (natural key) taken from the 'sub'-claim of the
    # id_token.
    'OIDC_RESOLVE_USER_FUNCTION': 'accounts.auth_backends.oidc_backend',

    # (Optional) Token prefix in JWT authorization header (default 'JWT')
    'JWT_AUTH_HEADER_PREFIX': config.oidc.bearer_auth_header_prefix,
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.debug

MEMCACHE_MAX_KEY_LENGTH = 1024
CACHES = {
    'default': {
        'BACKEND': 'django_prometheus.cache.backends.locmem.LocMemCache',
    }
}

ALLOWED_HOSTS = [
    config.fqdn,
    "localhost",
    "127.0.0.1"
]

REST_FRAMEWORK = {
    #    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    #    'PAGE_SIZE': 100
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.auth_classes.FlaggedTokenAuthentication',
        'oidc_auth.authentication.JSONWebTokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'accounts.permissions.AuthenticatedReadOnly'
    ]
}


AUTH_USER_MODEL = 'accounts.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_prometheus',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'netfields',
    'mptt',
    'sipam',
    'accounts',
]

CORS_ORIGIN_WHITELIST = [
    f"https://{config.fqdn}"
]
CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http://localhost:\d+$",
    r"^http://127.0.0.1:\d+",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'sipam.urls'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1)
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sipam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'NAME': config.database.name,
        'USER': config.database.user.name,
        'PASSWORD': config.database.user.password,
        'HOST': config.database.host,
        'PORT': config.database.port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
