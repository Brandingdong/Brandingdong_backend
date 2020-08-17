from .base import *
from .packages.phonenumber import *
from .packages.rest_framework import *
from .packages.auth import *

WSGI_APPLICATION = 'config.wsgi.production.application'
DEBUG = False
