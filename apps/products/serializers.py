from rest_framework import serializers

from apps.products.models import Category, SubCategory, Brand, Product, ProductOption, ProductInfo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category')


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'sub_category')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'brand')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sub_category = SubCategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = (
        'id', 'sub_category', 'category', 'brand', 'name', 'price', 'registered_at', 'quantity', 'delivery', 'status',
        'is_discount', 'discount_rate')


class ProductOptionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductOption
        fields = ('id', 'product', 'size', 'color')


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        models = ProductInfo
        fields = ('id', 'product', 'image', 'detail', 'info')
