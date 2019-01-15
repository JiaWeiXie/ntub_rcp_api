from .secret import SECRET_KEY
from .common import *

import os

head_name = os.environ.get('DJANGO_ENV', 'master')
develop_branches = ['master']

# Import setting
if head_name == 'develop':
    from .local_dev import *
elif head_name in develop_branches:
    from .develop import *
else:
    from .product import *

DATABASES = DB

INSTALLED_APPS += EXTRA_APPS

MIDDLEWARE = EXTRA_MIDDLEWARE + MIDDLEWARE

REST_FRAMEWORK = REST_SETTING

#  Setting extra variable
if head_name == 'develop':
    DEBUG = True
    CORS_ORIGIN_ALLOW_ALL = True
elif head_name in develop_branches:
    pass
else:
    pass

SIMPLE_JWT = {
    # timedelta(minutes=5)
    'ACCESS_TOKEN_LIFETIME': JWT_SETTING['ACCESS_TOKEN_LIFETIME'],
    'REFRESH_TOKEN_LIFETIME': JWT_SETTING['REFRESH_TOKEN_LIFETIME'],
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': JWT_SETTING['SLIDING_TOKEN_LIFETIME'],
    'SLIDING_TOKEN_REFRESH_LIFETIME': JWT_SETTING['SLIDING_TOKEN_REFRESH_LIFETIME'],
}
