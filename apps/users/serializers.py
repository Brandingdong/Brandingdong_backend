from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as DefaultTokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

USER = get_user_model()


class SignUpSerializer(RegisterSerializer):
    username = serializers.CharField()
    phonenumber = PhoneNumberField(required=True)

    def validate_username(self, username):
        if USER.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user is already registered with this username.")
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email

    def validate_phonenumber(self, phonenumber):
        if USER.objects.filter(phonenumber=phonenumber).exists():
            raise serializers.ValidationError("phonenumber already exists.")
        return phonenumber

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        data['password'] = data.pop('password1')
        data.pop('password2')

        return data

    def save(self, request):
        self.is_valid()
        validated_data = self.validated_data
        password = validated_data.pop('password')
        user = USER.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class JWTSerializer(serializers.Serializer):
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def get_refresh(self, obj):
        return str(self.get_token(obj['user']))

    def get_access(self, obj):
        return str(self.get_token(obj['user']).access_token)


class LoginSerializer(DefaultLoginSerializer):
    email = None
    username = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class PasswordChangeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)


##########################
### for Documentation
##########################

class TokenRefreshResultSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenRefreshSerializer(DefaultTokenRefreshSerializer):
    def to_representation(self, instance):
        return TokenRefreshResultSerializer(instance).data
