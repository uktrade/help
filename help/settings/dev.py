from ast import literal_eval
from .base import *

DEBUG = literal_eval(os.environ.get('DEBUG', 'True'))
ALLOWED_HOSTS = ['*']

ZENDESK_RESP_CODE = literal_eval(os.environ.get('ZENDESK_RESP_CODE', '201'))

USE_CAPTCHA = os.environ.get('USE_CAPTCHA', False) == 'True' or os.environ.get('USE_CAPTCHA', False) == '1'
CAPTCHA_SITE_KEY = os.environ.get('CAPTCHA_SITE_KEY', None)
CAPTCHA_SECRET_KEY = os.environ.get('CAPTCHA_SECRET_KEY', None)
