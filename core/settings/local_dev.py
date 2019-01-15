from datetime import timedelta

import dj_database_url

DB = {
    'default': dj_database_url.config(default='postgres://rcp:123@Admin@localhost:5432/rcp'),
}

EXTRA_APPS = [
    'drf_yasg',
    'corsheaders',
]

EXTRA_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

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
            'rest_framework.authentication.BasicAuthentication',
            'core.authentications.CsrfExemptSessionAuthentication',
            # 'rest_framework.authentication.SessionAuthentication',
        ],

}

JWT_SETTING = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=100),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=100),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=100),
}

