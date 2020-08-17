from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .validators import UnicodeUsernameValidator


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField(unique=True)

    REQUIRED_FIELDS = ['email', 'mobile']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, help_text='YYYY-MM-DD format')
    height = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()


class Address(models.Model):
    PROVINCE_CHOICES = [
        ('GW', '강원도'),
        ('GG', '경기도'),
        ('CB', '충청북도'),
        ('CN', '충청남도'),
        ('GB', '경상북도'),
        ('GN', '경상남도'),
        ('JB', '전라북도'),
        ('JN', '전라남도'),
        ('JJ', '제주특별자치도'),
        ('SE', '서울특별시'),
        ('BS', '부산광역'),
        ('DG', '대구광역시'),
        ('IC', '인천광역시'),
        ('GJ', '광주광역시'),
        ('DJ', '대전광역시'),
        ('US', '울산광역시'),
        ('SJ', '세종특별자치시'),
    ]

    user_profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    primary = models.BooleanField(default=False, help_text='기본 배송지')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=30)
    street_name_address = models.CharField('도로명 주소', max_length=70, blank=True)
    land_lot_number_address = models.CharField('지번 주소', max_length=70, blank=True)

    def save(self, *args, **kwargs):
        # primary address(기본 주소)는 반드시 하나만 존재
        # 새로운 주소가 primary로 추가되면 기본 주소는 primary=False로 변경
        if self.primary:
            try:
                primary_address = Address.objects.get(user_profile=self.user_profile)
                if self != primary_address:
                    primary_address.primary = False
                    primary_address.save()
            except Address.DoesNotExist:
                pass
        super(Address, self).save(*args, **kwargs)
