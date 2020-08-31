from .base import *
from .packages.auth import *
from .packages.rest import *
from .packages.s3 import *

WSGI_APPLICATION = 'config.wsgi.develop.application'
ALLOWED_HOSTS = ['*']
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

INSTALLED_APPS += [
    'django_extensions',
]

DEBUG = True