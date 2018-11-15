# -*- coding: utf-8 -*-
"""
Django settings for RoleJobs project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from rolejobs.local_settings import  *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_BASE = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^a3!45fn%7b6)xdt*&tqg-89(4%*^z(ms+#dxyk9vhxhkbmr$i'

ALLOWED_HOSTS = []

SITE_ID = 5

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Geo
    'cities_light',

    # tags
    'taggit',
    'taggit_serializer',

    # Forms
    'crispy_forms',
    'crispy_forms_foundation',
    'widget_tweaks',

    # Angular integration
    'djng',

    # API
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rest_framework_filters',

    # Auth
    'rest_auth',
    # 'social.apps.django_app.default',
    'email_auth',
    'allauth',
    'allauth.account',
    # 'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',

    # Sanitize
    'sanitizer',

    # Own
    'utils',
    'emailspool',
    'rolejobs_api',
    'accounts',
    'postulant',
    'employer',
    'localidades',
    'jobs',
    'education',
    'contact',
    'avatars',
    'usermessages',
    'courses',
    'geo',
]

# Add 'foundation-5' layout pack
CRISPY_ALLOWED_TEMPLATE_PACKS = (
    'bootstrap', 'uni_form', 'bootstrap3', 'foundation-5')
# Default layout to use with "crispy_forms"
CRISPY_TEMPLATE_PACK = 'foundation-5'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rolejobs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.core.context_processors.i18n",
                "django.core.context_processors.tz",
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rolejobs.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = 'es'

LANGUAGES = (
    ('es', u'Español'),
    ('en', u'English'),
)
DEFAULT_LANGUAGE = 1
# Location of translation files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    STATIC_BASE,
    os.path.join(BASE_DIR, 'dist'),
    os.path.join(BASE_DIR, 'node_modules'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "/media/"

# Fixtures
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'data'),
)

# Users
AUTH_USER_MODEL = 'accounts.User'

# django-allauth config
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_ADAPTER = 'accounts.adapter.SocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True

# Use UserProfile!
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
}

# Set login serializer
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'accounts.serializers.LoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'accounts.serializers.PasswordResetSerializer',
}

# Auth options
OLD_PASSWORD_FIELD_ENABLED = True,
LOGOUT_ON_PASSWORD_CHANGE = False

STANDAR_PAGE_SIZE = 5
STANDAR_MAX_PAGE_SIZE = 40

# Cities light
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['es', 'en']
