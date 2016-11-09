from .base import *

DEBUG = False
ALLOWED_HOSTS = ['contact-us.export.great.gov.uk']

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

USE_CAPTCHA = os.environ.get('USE_CAPTCHA', False) == 'True' or os.environ.get('USE_CAPTCHA', False) == '1'
CAPTCHA_SITE_KEY = os.environ.get('CAPTCHA_SITE_KEY', None)
CAPTCHA_SECRET_KEY = os.environ.get('CAPTCHA_SECRET_KEY', None)
