# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_auth.registration.views import RegisterView, LoginView as DefaultLoginView
from rest_auth.views import LogoutView as DefaultLogoutView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from users.utils import get_random_alphanumeric_string, send_random_code_email
from .serializers import SignUpSerializer, LoginSerializer, PasswordResetSerializer, PasswordChangeSerializer

USER = get_user_model()


class SignupView(RegisterView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(DefaultLoginView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]


class LogoutView(DefaultLogoutView):
    def _allowed_methods(self):
        return ['GET']


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
