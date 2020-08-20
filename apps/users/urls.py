from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import SignupView, LoginView, LogoutView, PasswordResetView, PasswordChangeView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/password/reset/', PasswordResetView.as_view(), name='pw_reset'),
    path('auth/password/change/', PasswordChangeView.as_view(), name='pw_change'),
]
