from datetime import timedelta

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# DJANGO_REST_AUTH
ACCOUNT_LOGOUT_ON_GET = True
REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    'JWT_SERIALIZER': 'users.serializers.JWTSerializer',
}

REST_AUTH_REGISTER_SERIALIZER = {
    'REGISTER_SERIALIZER': 'users.serializers.SingUpSerializer',
}
