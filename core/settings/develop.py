import sys
import logging
import dj_database_url

from datetime import timedelta

logging.basicConfig(stream=sys.stderr)

DB = {
    'default': dj_database_url.config(default='postgres://rcp:123@Admin@db:5432/rcp'),
}

EXTRA_APPS = [
    'drf_yasg',
]

EXTRA_MIDDLEWARE = []

REST_SETTING = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
            # 'rest_framework.authentication.BasicAuthentication',
            'core.authentications.CsrfExemptSessionAuthentication',
            # 'rest_framework.authentication.SessionAuthentication',
        ],

}

JWT_SETTING = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=100),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=100),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=100),
}
