from ast import literal_eval
from .base import *


DEBUG = literal_eval(os.environ.get('DEBUG', 'True'))
ALLOWED_HOSTS = ['*']

ZENDESK_RESP_CODE = literal_eval(os.environ.get('ZENDESK_RESP_CODE', '201'))
