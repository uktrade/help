from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'contact-us.export.great.gov.uk',
    'enav-help.cloudapps.digital'
]

CSRF_TRUSTED_ORIGINS = [
    'contact-us.export.great.gov.uk'
]

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
