"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from rest_framework import routers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.settings import head_name, develop_branches
from core.authentications import CsrfExemptSessionAuthentication
from account import urls as account_urls
from curriculum import urls as curriculum_urls
from roll_call import urls as roll_call_urls
from announcement import urls as announcement_urls

# REST API Routing
main_router = routers.SimpleRouter()
app_urlpatterns = []  # init app_urlpatterns
app_urls = [  # include app's urls
    account_urls,
    curriculum_urls,
    roll_call_urls,
    announcement_urls,
]
for app_url in app_urls:
    for route_url in app_url.routers_list:
        main_router.register('{0}/{1}'.format(app_url.base_url, route_url.get('prefix')),
                             viewset=route_url.get('viewset'),
                             base_name=route_url.get('base_name'))
    if len(app_url.urlpatterns):
        app_urlpatterns.append(
            path('api/{}/'.format(app_url.base_url), include(app_url))
        )

schema_view = get_schema_view(
   openapi.Info(
      title="RCP API",
      default_version='v1',
      description="點名系統API文件",
      terms_of_service="NTUB IMD",
      contact=openapi.Contact(email="10446005@ntub.edu.tw"),
   ),
   public=True,
   permission_classes=(IsAuthenticated,),
   authentication_classes=(BasicAuthentication, CsrfExemptSessionAuthentication, JWTTokenUserAuthentication),
)


# App in develop time
if head_name == 'develop':
    from django.contrib import admin
    extra_urls = [
        path('admin/', admin.site.urls),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    ]
elif head_name in develop_branches:
    from django.contrib import admin
    extra_urls = [
        path('admin/', admin.site.urls),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    ]
else:
    extra_urls = []

# Main URLs
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include(main_router.urls))
] + app_urlpatterns + extra_urls
