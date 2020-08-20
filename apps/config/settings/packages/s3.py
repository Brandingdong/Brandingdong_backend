import os

import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env_path = os.path.dirname(os.path.dirname(BASE_DIR)) + '/.env'
enf_file = environ.Env.read_env(env_file=env_path)

# S3
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = os.environ['AWS_S3_REGION_NAME']
AWS_DEFAULT_ACL = None

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

# s3 static settings
STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'config.storages.S3StaticStorage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

# s3 media settings
DEFAULT_FILE_STORAGE = 'config.storages.S3MediaStorage'
MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
