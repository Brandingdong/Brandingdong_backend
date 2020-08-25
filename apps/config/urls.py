"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Brandingdong API",
        default_version='v1',
        description='''Repository: https://github.com/Brandingdong/Brandingdong_backend
        \n 브랜드 클론 코딩 API''',
        terms_of_service="",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('events/', include('events.url') )
]
