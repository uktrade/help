from .base import *

ALLOWED_HOSTS = [
    'contact-us.export.demo.uktrade.io',
    '.herokuapp.com',
]

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
