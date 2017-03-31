from .base import *

DEBUG = False
ALLOWED_HOSTS = ['contact-us.export.staging.uktrade.io']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
