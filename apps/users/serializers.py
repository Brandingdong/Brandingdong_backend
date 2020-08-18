from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

USER = get_user_model()


class SignUpSerializer(RegisterSerializer):
    phonenumber = PhoneNumberField()

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            "phonenumber": self.validated_data.get('phonenumber', ''),
        }

    def validate_phonenumber(self, attrs):
        if USER.objects.filter(phonenumber=attrs).exists():
            raise serializers.ValidationError("phonenumber already exists.")
