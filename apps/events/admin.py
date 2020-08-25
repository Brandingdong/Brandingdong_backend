from django.contrib import admin

# Register your models here.
from events.models import Events


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'images', 'created_at', 'modified_at']
    search_fields = ['images']
    ordering = ['-id', 'created_at']


admin.site.register(Events, PostAdmin)
