from django.contrib import admin

# Register your models here.
from products.models import Category


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']
#     search_fields = ['name']
#     ordering = ['-id']
#
#
# admin.site.register(Category, CategoryAdmin)
