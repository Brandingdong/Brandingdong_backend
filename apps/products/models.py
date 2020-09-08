from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)


class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=32)


class Brand(models.Model):
    brand_cate = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=32)
    intro = models.CharField(max_length=100, blank=True)
    brand_img = models.ImageField(upload_to='brand_img', verbose_name='이미지', blank=True)


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

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    discount_rate = models.DecimalField(max_digits=3, decimal_places=2)
    sales_count = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=3, choices=DELIVERY_CHOICES, default='OD')
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
    text = models.TextField(blank=True)


class SellingInfo(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    _company_name = models.CharField('상호명', max_length=20, blank=True)
    _representative = models.CharField('대표자', max_length=10, blank=True)
    _license_num = models.CharField('사업자등록번호', max_length=100, blank=True)
    _mail_order_num = models.CharField('통신판매업번호', max_length=100, blank=True)
    _biz_location = models.CharField('사업장소재지', max_length=100, blank=True)
    _biz_hour = models.CharField('영업시간', max_length=255, blank=True)
    _company_email = models.CharField('메일', max_length=255, blank=True)
    _company_call = models.CharField('전화번호', max_length=255, blank=True)
    model_size = models.TextField('모델사이즈정보', max_length=255, blank=True)
    _shipping_info = models.TextField('배송정보', max_length=255, blank=True)
    _exchange_refund_info = models.TextField('교환/환불정보', max_length=255, blank=True)
    _product_notice = models.CharField('상품정보고시', max_length=100, blank=True)

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

    @property
    def business_hour(self):
        if not self._business_hour:
            return (f'주중 10:00 AM ~ 10:00 PM, 주말 및 공휴일 휴무')
        return self._business_hour

    @business_hour.setter
    def business_hour(self, value):
        self._business_hour = value

    @property
    def company_email(self):
        if not self._company_email:
            return (f'이메일 : brandiffcs@brandi.co.kr')
        return self._company_email

    @company_email.setter
    def company_email(self, value):
        self._company_email = value

    @property
    def company_call(self):
        if not self._company_call:
            return (f'전화번호 : 1577-3452')
        return self._company_call

    @company_call.setter
    def company_call(self, value):
        self._company_call = value

    @property
    def shipping_info(self):
        if not self._shipping_info:
            return (
                f'브랜디배송 고객센터 운영시간\n'
                f'일반배송 - 10시 ~ 17시\n'
                f'하루배송 - 10시 ~ 22시\n'
                f'18시 이후에는 하루배송 문의만 가능합니다.\n'
                f'주말, 공휴일 휴무 /점심시간 12시30분~13시30분 /저녁시간 17시~18시\n'
                f'<일반배송>\n'
                f'택배사는 우체국 택배를 이용하고 있습니다.\n'
                f'도서산간 지역의 배송비 추가는 별도로 없습니다.\n'
                f'결제 후 평균 2~5일 소요될 수 있으며(주말, 공휴일 제외) 거래처 상황에 따라 변동될 수 있습니다.\n'
                f'주문 급증, 인기 상품의 경우 기본 배송기간 이상 소요될 수 있는 점 양해 부탁드립니다.\n'
                f'기본 배송일 이상 혹은 품절된 상품은 개별 연락 (알림톡, 문자) 드리고 있습니다.\n'
                f'대체 옵션이 없는 품절 상품은 빠른 처리를 도와드리기 위해 알림톡 연락 후 주문 취소 처리를 진행해드리고 있습니다.\n'
                f'<하루배송>\n'
                f'새벽 도착/저녁 도착은 협력업체를 이용하고 있습니다.\n'
                f'배송지가 서울인 경우 하루배송 상품 2개 이상 주문 시 새벽 도착/저녁 도착 서비스 이용 가능합니다.\n'
                f'서울이 아닐 경우 최대 2,000포인트 적립 가능하며 오후 2시 이전 결제 완료해 주시면 당일 출고 가능합니다!\n'
                f'▷새벽 도착\n'
                f'당일 오전 8시~오후 8시59분 결제 시 다음날 오전 7시까지 도착 보장\n'
                f'▷저녁 도착\n'
                f'전일 오후 9시~당일 오전 7시59분 결제 시 당일 오후 8시까지 도착 보장\n'
                f'배송 과정에서 특이사항 발생될 경우 알림톡 전송 도와드리고 있습니다.'
            )
        return self._shipping_info

    @shipping_info.setter
    def shipping_info(self, value):
        self._shipping_info = value

    @property
    def exchange_refund_info(self):
        if not self._exchange_refund_info:
            return (
                f'상품가치가 현저히 훼손된 경우를 제외한 모든 사유에 대해 환불이 가능합니다.\n'
                f'환불요청 가능 기간은 상품 수령 후(배송완료 시점으로부터) 7일 이내입니다.\n'
                f'교환/환불이 발생하는 경우 그 원인을 제공한 자가 배송비를 부담합니다.\n'
                f'- 고객변심 : 최초 배송비+반품 배송비+(교환의 경우) 교환 배송비는 고객이 부담\n'
                f'- 판매자귀책 : 최초 배송비+반품 배송비+(교환의 경우) 교환 배송비는 판매자가 부담\n'
                f'다음의 경우는 예외적으로 교환 및 환불이 불가능합니다.\n'
                f'- 상품가치가 소비자의 귀책사유로 인해 현저하게 감소한 경우\n'
                f'- 소비자 과실로 인한 옷의 변색(예 : 착색, 화장품, 오염 등)\n'
                f'- 착용으로 인한 니트류 상품의 늘어남 발생 및 가죽 제품의 주름 발생\n'
                f'- 기타 착용 흔적 : 택 제거 등\n'
                f'- 구매확정된 주문의 경우\n'
                f'- 귀금속류의 경우는 소비자분쟁조정기준에 의거 교환만 가능합니다.\n'
                f'(단, 함량미달의 경우에는 환불이 가능함)\n'
                f'브랜디배송 제품은 환불 요청 접수 후 평일 기준 1~3일 내로 자동 회수 접수 및 기사님의 회수 방문이 진행됩니다.\n'
                f'판매자배송 제품과 합반품은 불가능하며 배송비 부담 후 반송될 수 있습니다.\n'
                f'교환/반품 신청 후 장기간(2주 이상) 상품이 저희 측에 도착하지 않을 경우 처리가 어려울 수 있습니다.\n'
                f'[단순 변심]\n'
                f'단순 변심의 교환이나 반품의 경우 왕복 택배비(5,000원)를 아래의 계좌로 입금해 주셔야 합니다.\n'
                f'[계좌 정보 :입금 계좌 : 022-105089-04-069 기업은행 / 주식회사 브랜디]\n'
                f'*택배비 입금 시 성함과 휴대폰 뒷자리를(4자리)(ex-홍길동 5349) 입력하시면 더 빠른 처리가 가능합니다.\n'
                f'상품의 하자 및 오배송으로 인한 교환/반품의 경우는 택배비가 발생되지 않습니다.\n'
                f'상품 하자가 있는 경우에는 상품을 공급받은 날부터 3개월 이내로서, 그 사실을 안 날 또는 알 수 있었던 날부터 30일 이내 청약철회가 가능합니다.\n'
                f'비키니/속옷 상품 반품 시, 상품에 부착 되어 있는 위생테이프 제거 시 반품 불가합니다.\n'
                f'상의 상품 반품 시, 캡 미동봉시 반품 불가합니다. (동봉 되어 있는 상품인 경우)\n'
                f'[교환∙반품 방법]\n'
                f'*동봉된 교환∙반품 신청서를 참조하세요\n'
                f'[택배사 수거 접수 방법]\n'
                f'합반품 및 직접 반송하실 경우 환불요청 버튼 누르기 전, 꼭! Q&A나 고객센터(1577-3452)로 말씀해 주셔야 중복접수가 되지 않습니다.\n'
                f'직접 반송하실 경우 하단의 배송센터 주소지로 보내주셔야 처리가 가능하며, 다른 주소지로 보내실 경우 반송처리되실 수 있습니다.\n'
                f'타 택배 이용 시 반품 택배비는 고객님께서 선불로 부담하신 후 2,500원을 입금해 주셔야 하며,\n'
                f'불량 및 오배송의 경우에도 직접 부담하셔야 합니다.\n'
                f'(추후 \'환불요청\'이 되어있지 않은 상품 도착 시 반송될 수 있으니 꼭 \'환불요청\' 상태로 변경해 주시기 바랍니다)\n'
                f'고객센터(환불 및 배송문의) 1577-3452\n'
                f'영업시간 10:00-17:00 점심시간 12:30-13:30 (주말, 공휴일 제외)\n'
                f'배송비 입금 계좌 : 0 2 2 - 1 0 5 0 8 9 - 0 4 - 0 6 9 기업은행 / 주식회사 브랜디\n'
                f'교환/반품 주소지 서울 중구 소공로 70 브랜디 물류센터'
            )
        return self._exchange_refund_info

    @exchange_refund_info.setter
    def exchange_refund_info(self, value):
        self._exchange_refund_info = value

    @property
    def product_notice(self):
        if not self._product_notice:
            return ('상품상세 참조')
        return self._product_notice

    @product_notice.setter
    def product_notice(self, value):
        self._product_notice = value


class ProductImage(models.Model):
    product = models.ForeignKey('Product', blank=True, on_delete=models.CASCADE, verbose_name='상품이미지')
    image = models.ImageField(upload_to='main_img', verbose_name='이미지', blank=True)


class ProductInfoImage(models.Model):
    product_info = models.ForeignKey('ProductInfo', blank=True, on_delete=models.CASCADE, verbose_name='상품정보이미지')
    image = models.ImageField(upload_to='info_img', verbose_name='이미지', blank=True)
