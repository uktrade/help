from ast import literal_eval
from .base import *


DEBUG = literal_eval(os.environ.get('DEBUG', 'True'))
ALLOWED_HOSTS = ['*']

ZENDESK_RESP_CODE = literal_eval(os.environ.get('ZENDESK_RESP_CODE', '201'))

USE_CAPTCHA = True
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
