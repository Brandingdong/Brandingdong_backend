from .base import *
from .packages.phonenumber import *
from .packages.rest_framework import *
from .packages.auth import *

WSGI_APPLICATION = 'config.wsgi.develop.application'
ALLOWED_HOSTS = ['*']
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
