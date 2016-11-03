from .base import *

DEBUG = False
ALLOWED_HOSTS = ['contact-us.export.great.gov.uk']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

# XXX: This needs to be made longer once it is confirmed it works as desired
SECURE_HSTS_SECONDS = 60

SECURE_SSL_REDIRECT = True
