from django.contrib import admin

# Register your models here.
from products.models import Category, Product, SubCategory, Brand


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['-id']


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'sub_name']
    ordering = ['-id']


admin.site.register(SubCategory, SubCategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand_cate', 'name', 'intro', 'brand_img']
    ordering = ['-id']


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'sub_category', 'brand', 'name', 'price', ]
    ordering = ['-id']


admin.site.register(Product, ProductAdmin)
