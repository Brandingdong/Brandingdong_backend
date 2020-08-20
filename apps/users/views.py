# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_auth.registration.views import RegisterView, LoginView as DefaultLoginView
from rest_auth.views import LogoutView as DefaultLogoutView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView as DefaultTokenRefreshView, \
    TokenVerifyView as DefaultTokenVerifyView

from users.utils import get_random_alphanumeric_string
from .serializers import SignUpSerializer, LoginSerializer, PasswordResetSerializer, PasswordChangeSerializer, \
    JWTSerializer, TokenRefreshResultSerializer, TokenRefreshSerializer

USER = get_user_model()


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Sign Up',
    operation_description='회원가입',
    responses={201: JWTSerializer()},
))
class SignupView(RegisterView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Log In',
    operation_description='로그인',
    responses={200: JWTSerializer()},
))
class LoginView(DefaultLoginView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='Log Out',
    operation_description='로그아웃',
))
class LogoutView(DefaultLogoutView):
    def _allowed_methods(self):
        return ['GET']


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Token Refresh',
    operation_description='Refresh Token을 통해 만료된 Access Token 재발급',
    responses={200: TokenRefreshResultSerializer()}
))
class TokenRefreshView(DefaultTokenRefreshView):
    serializer_class = TokenRefreshSerializer


@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='Access Token Verify',
    operation_description='Access Token이 유효한지 확인',
    responses={200: ''}
))
class TokenVerifyView(DefaultTokenVerifyView):
    pass


class PasswordResetView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        try:
            user = USER.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValidationError("User does not exist")

        if user.email != email:
            raise ValidationError("email not matched for user")

        random_code = get_random_alphanumeric_string(8)
        user.set_password(random_code)
        user.save()

        # send_random_code_email(email, random_code, username)

        ret_dict = dict()
        ret_dict['username'] = username
        ret_dict['random_code'] = random_code
        # ret_dict['detail'] = f'email sent to {email}'

        return Response(ret_dict)


class PasswordChangeView(CreateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        current_password = request.data.get('current_password', '')
        password1 = request.data.get('password1', '')
        password2 = request.data.get('password2', '')

        try:
            user = USER.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValidationError("User Does Not Exist.")

        if not check_password(current_password, user.password):
            raise ValidationError("Current Password Not Matching.")

        if password1 != password2:
            raise ValidationError("The two password fields didn't match.")

        user.set_password(password1)
        user.save()

        ret_dict = dict()
        ret_dict['username'] = username
        ret_dict['detail'] = 'password changed'

        return Response(ret_dict)
