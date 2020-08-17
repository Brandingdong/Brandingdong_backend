from django.urls import path

from .views import GoogleLoginView

urlpatterns = [
    path('login/google/', GoogleLoginView.as_view(), name='google_login'),
]
