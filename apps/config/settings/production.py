from .base import *
from .packages.auth import *
from .packages.rest import *
from .packages.s3 import *


WSGI_APPLICATION = 'config.wsgi.production.application'
ALLOWED_HOSTS = ['*']
DEBUG = False

