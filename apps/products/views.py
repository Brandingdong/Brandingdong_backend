from rest_framework import viewsets, pagination

from products.models import Product, Category, SubCategory, Brand, ProductOption, ProductImage, ProductInfoImage, \
    ProductInfo, SellingInfo
from products.serializers import ProductSerializer, CategorySerializer, SubCategorySerializer, BrandSerializer, \
    ProductImageSerializer, ProductOptionSerializer, ProductInfoImageSerializer, ProductInfoSerializer, \
    SellingInfoSerializer

'''카테고리'''


class ProductPagination(pagination.CursorPagination):
    page_size = 30
    ordering = 'created_at'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


'''서브카테고리'''


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all().select_related('category')
    serializer_class = SubCategorySerializer


'''브랜드'''


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


'''제품상세'''


class ProductOptionViewSet(viewsets.ModelViewSet):
    queryset = ProductOption.objects.all()
    serializer_class = ProductOptionSerializer


'''제품메인이미지'''


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


'''제품소개이미지'''


class ProductInfoImageViewSet(viewsets.ModelViewSet):
    queryset = ProductInfoImage.objects.all()
    serializer_class = ProductInfoImageSerializer


'''제품뷰셋'''


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('brand').prefetch_related('main_img')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


'''제품정보'''


class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all().prefetch_related('info_img')
    serializer_class = ProductInfoSerializer


'''주문정보'''


class SellingInfoViewSet(viewsets.ModelViewSet):
    queryset = SellingInfo.objects.all()
    serializer_class = SellingInfoSerializer
