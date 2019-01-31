# -*- encoding: utf-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'RoleJobs2',
        'USER': 'postgres',
        'PASSWORD': 'Riddle**2001',
        'HOST': 'localhost',
        'PORT': '5432'
        # 'POSRT': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Buenos_Aires'

# Perms

ADMINS = (
    ('Exos', 'ogentilezza@gentisoft.com'),
)

# Email configuration

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = 'correo.matcom.uh.cu' #EMAIL_HOST = 'mail.rolejobs.net'
EMAIL_HOST_USER = 'ismel@matcom.uh.cu' #EMAIL_HOST_USER = 'noreply@rolejobs.net'
EMAIL_HOST_PASSWORD = 'lemsywaylocuramix' #EMAIL_HOST_PASSWORD = 'fW_@elegOHn7'
EMAIL_PORT = 465 #EMAIL_PORT = 465
#EMAIL_USE_TLS = True
#EMAIL_FROM = 'RoleJobs <noreply@rolejobs.com>'

#CONTACT_EMAIL = "oscar@gentisoft.com"

FORGOT_EMAIL_EXPIRE_TIME = 7  # 7 dias

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d ' +
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

SITE_BASE_URL = "http://localhost:8000"
