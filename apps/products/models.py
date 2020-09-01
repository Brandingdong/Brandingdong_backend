from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)


class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)


class Brand(models.Model):
    name = models.CharField(max_length=32)


class Product(models.Model):
    DELIVERY_CHOICES = [
        ('OD', 'OneDayDelivery'),
        ('REG', 'RegularDelivery'),
    ]
    SALE_STATUS = [
        ('FS', 'ForSale'),
        ('SS', 'StopSale'),
        ('SO', 'SoldOut'),
    ]

    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=3, choices=DELIVERY_CHOICES, default='OD')
    discount_rate = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=SALE_STATUS, blank=True, default='FS')


class ProductOption(models.Model):
    SIZE_CHOICES = [
        ('XS', 'X-SMALL'),
        ('S', 'SMALL'),
        ('M', 'MEDIUM'),
        ('L', 'LARGE'),
    ]
    COLOR_CHOICES = [
        ('WH', 'WHITE'),
        ('BL', 'BLACK'),
        ('GY', 'GRAY'),
        ('RD', 'RED'),
        ('BL', 'BLUE'),
        ('GR', 'GREEN'),
        ('YL', 'YELLOW'),
        ('PP', 'PURPLE'),
        ('BR', 'BROWN'),
        ('etc', 'etc'),
    ]

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=True)
    color = models.CharField(max_length=3, choices=COLOR_CHOICES, blank=True)
    stock = models.PositiveIntegerField(default=0)


class ProductInfo(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    detail = models.TextField(blank=True)


class SellingInfo(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    _company_name = models.CharField('상호명', max_length=20, blank=True)
    _representative = models.CharField('대표자', max_length=10, blank=True)
    _license_num = models.CharField('사업자등록번호', max_length=100, blank=True)
    _mail_order_num = models.CharField('통신판매업번호', max_length=100, blank=True)
    _biz_location = models.CharField('사업장소재지', max_length=100, blank=True)
    customer_service = models.TextField('스토어고객센터', max_length=255, blank=True)
    model_size = models.TextField('모델사이즈정보', max_length=255, blank=True)
    shipping_info = models.TextField('배송정보', max_length=255, blank=True)
    exchange_refund_info = models.TextField('교환/환불정보', max_length=255, blank=True)
    product_notice = models.CharField('상품정보고시', max_length=100, blank=True)

    '''
    SellerInfo 기본값
    '''

    @property
    def company_name(self):
        if not self._company_name:
            return ('주식회사 브랜디')
        return self._company_name

    @company_name.setter
    def company_name(self, value):
        self._company_name = value

    @property
    def representative(self):
        if not self._representative:
            return ('서정민')
        return self._representative

    @representative.setter
    def representative(self, value):
        self._representative = value

    @property
    def license_num(self):
        if not self._license_num:
            return ('220-88-93187')
        return self._license_num

    @license_num.setter
    def license_num(self, value):
        self._license_num = value

    @property
    def mail_order_num(self):
        if not self._mail_order_num:
            return ('제2016-서울강남-00359호')
        return self._mail_order_num

    @mail_order_num.setter
    def mail_order_num(self, value):
        self._mail_order_num = value

    @property
    def biz_location(self):
        if not self._biz_location:
            return ('04535 ) 서울 중구 소공로 70 (충무로1가, 서울중앙우체국청사)브랜디 물류센터')
        return self._biz_location

    @biz_location.setter
    def biz_location(self, value):
        self._biz_location = value


class ProductImage(models.Model):
    product = models.ForeignKey('Product', blank=True, on_delete=models.CASCADE, verbose_name='상품이미지')
    image = models.ImageField(upload_to='products', verbose_name='이미지', blank=True)


class ProductInfoImage(models.Model):
    product = models.ForeignKey('Product', blank=True, on_delete=models.CASCADE, verbose_name='상품정보이미지')
    image = models.ImageField(upload_to='products', verbose_name='이미지', blank=True)
