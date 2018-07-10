from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'contact-us.export.staging.uktrade.io',
    'enav-help-staging.cloudapps.digital'
]

CSRF_TRUSTED_ORIGINS = [
    'contact-us.export.staging.uktrade.io'
]

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]


SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
