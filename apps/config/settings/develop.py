from .base import *
from .packages.phonenumber import *

WSGI_APPLICATION = 'config.wsgi.develop.application'
ALLOWED_HOSTS = ['*']
