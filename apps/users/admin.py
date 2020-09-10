from django.contrib import admin

# Register your models here.
from django.contrib import admin

from users.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phonenumber', 'is_staff', 'date_joined']
    search_fields = ['username']
    ordering = ['-id', 'date_joined']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'gender', 'date_of_birth', 'height', 'weight']
    search_fields = ['user']
    ordering = ['-id']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'primary', 'province', 'city', 'street_name_address',
                    'land_lot_number_address']
    search_fields = ['user_profile']
    ordering = ['-id']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
