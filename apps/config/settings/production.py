from .base import *
from .packages.auth import *
from .packages.rest import *

WSGI_APPLICATION = 'config.wsgi.production.application'
DEBUG = False

