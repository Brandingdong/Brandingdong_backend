from rest_framework import serializers

from products.models import Category, SubCategory, Brand, Product, ProductOption, ProductInfo, ProductImage, \
    ProductInfoImage, SellingInfo

'''카테고리'''


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


'''서브 카테고리'''


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'sub_name')
        read_only_fields = (
            'category',
        )


'''브랜드 카테고리'''


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


'''제품상세 옵션 (사이즈, 색상, 재고등)'''


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('id', 'product', 'color', 'size', 'stock')


'''제품페이지 상단 메인이미지'''


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'pk',
            'image',
        )


'''제품정보이미지'''


class ProductInfoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfoImage
        fields = (
            'pk',
            'image',
        )


'''제품 페이지 시리얼라이져'''


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.IntegerField()
    main_img = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'sub_category',

            'main_img',
            'brand',
            'name',

            'price',
            'discount_rate',
            'sales_count',
            'delivery',

            'status',
            'created_at',
            'modified_at',
        )
        read_only_fields = (
            'main_img',
        )

    def create(self, validated_data):
        brand = validated_data.pop('brand')
        validated_data['brand_id'] = brand
        # brand = brand = Brand.objects.get_or_404(id=brand_id)
        # validated_data['brand'] = brand
        return super().create(validated_data)


'''제품 하단 정보 시리얼라이저'''


class ProductInfoSerializer(serializers.ModelSerializer):
    info_img = ProductInfoImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductInfo

        fields = (
            'id',
            'product',
            'info_img',
            'text',
        )
        read_only_fields = (
            'info_img',
        )


'''제품 주문 정보 시리얼라이저'''


class SellingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellingInfo
        fields = ('id',
                  'product',
                  'company_name',
                  'representative',
                  'license_num',
                  'mail_order_num',
                  'biz_location',
                  'biz_hour',
                  'company_email',
                  'company_call',
                  'model_size',
                  'shipping_info',
                  'exchange_refund_info',
                  'product_notice',
                  )
