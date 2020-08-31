from rest_framework import viewsets

from apps.products.models import Product, Category, SubCategory, Brand
from apps.products.serializers import ProductSerializer, CategorySerializer, SubCategorySerializer, BrandSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryModelViewSet(viewsets.ModelViewset):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryModelViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class BrandModelViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
