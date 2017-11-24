"""
Django settings for help project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'directory_header_footer',
    'contact',
    'thumber',
    'captcha',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ip_restriction.IpWhitelister',
]

ROOT_URLCONF = 'help.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'directory_header_footer.context_processors.urls_processor',
                'sso.context_processors.sso_processor',
                'contact.context_processors.hosts',
            ],
        },
    },
]

WSGI_APPLICATION = 'help.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_HTTPONLY = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

ZENDESK_URL = os.environ.get('ZENDESK_URL')
ZENDESK_USER = os.environ.get('ZENDESK_USER')
ZENDESK_TOKEN = os.environ.get('ZENDESK_TOKEN')
ZENDESK_TEST_URL = os.environ.get('ZENDESK_TEST_URL')

USE_CAPTCHA = os.environ.get('USE_CAPTCHA', 'false').lower() == 'true' or os.environ.get('USE_CAPTCHA', False) == '1'

RECAPTCHA_PUBLIC_KEY = os.environ.get('CAPTCHA_SITE_KEY', None)
RECAPTCHA_PRIVATE_KEY = os.environ.get('CAPTCHA_SECRET_KEY', None)
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = True


RESTRICT_IPS = os.environ.get('RESTRICT_IPS', '').lower() == 'true' or os.environ.get('RESTRICT_IPS') == '1'

COMPANIES_HOUSE_API_KEY = os.environ.get('COMPANIES_HOUSE_KEY')

RATELIMIT_STATUS_CODE = 429  # For the brake module, unless specified (weirdly) uses 403

# Hosts for various services, used in templates
SOO_HOST = os.environ.get('SOO_HOST', 'https://selling-online-overseas.export.great.gov.uk/')
HELP_HOST = os.environ.get('HELP_HOST', 'https://contact-us.export.great.gov.uk/')
SSO_HOST = os.environ.get('SSO_HOST', 'https://sso.trade.great.gov.uk/')
PROFILE_HOST = os.environ.get('PROFILE_HOST', 'https://profile.great.gov.uk/')

ZENDESK_RESP_CODE = os.environ.get('ZENDESK_RESP_CODE', None)

# SSO
SSO_PROXY_LOGIN_URL = os.environ.get(
    'SSO_PROXY_LOGIN_URL', 'http://sso.trade.great.dev:8004/accounts/login/'
)
SSO_PROXY_SIGNUP_URL = os.environ.get(
    'SSO_PROXY_SIGNUP_URL', 'http://sso.trade.great.dev:8004/accounts/signup/'
)
SSO_PROFILE_URL = os.environ.get(
    'SSO_PROFILE_URL',
    'http://profile.trade.great.dev:8006/selling-online-overseas/'
)
SSO_PROXY_LOGOUT_URL = os.environ.get(
    'SSO_PROXY_LOGOUT_URL', 'http://sso.trade.great.dev:8004/accounts/'
    'logout/?next=http://contact.trade.great.dev:8008'
)
