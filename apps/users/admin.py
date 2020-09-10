from django.contrib import admin

# Register your models here.
from django.contrib import admin

from users.models import *

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Address, UserAdmin)
