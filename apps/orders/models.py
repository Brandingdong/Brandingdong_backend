from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from products.models import Product, ProductOption

User = get_user_model()


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('NAVER', '네이버페이'),
        ('CACAO', '카카오페이'),
        ('TOSS', '토스'),
        ('CREDIT', '신용카드'),
        ('BANKBOOK', '무통장입금'),
        ('PHONE', '휴대폰결제'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('이름', max_length=50)
    phone = PhoneNumberField('휴대폰', max_length=250)
    email = models.EmailField('이메일', max_length=250)

    receiver = models.CharField('수령인', max_length=50)
    receiver_phone = PhoneNumberField('수령인_휴대폰')
    zip_code = models.CharField('우편번호', max_length=250)
    destination = models.CharField('주소', max_length=250)
    detail_destination = models.CharField('상세주소', max_length=250)

    delivery_request = models.CharField('배송요청사항', max_length=250, blank=True)

    point_use = models.PositiveIntegerField('포인트 사용', default=0)
    payment = models.CharField('결제 수단', choices=PAYMENT_CHOICES, max_length=100)

    total_price = models.PositiveIntegerField('상품금액', default=0)
    total_delivery_fee = models.PositiveIntegerField('배송비', default=0)
    final_price = models.PositiveIntegerField('결제 예상금액', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class OrderItems(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='주문', related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        order_item = Order.objects.get(pk=self.order.pk)
        product_item = Product.objects.get(pk=self.product.pk)
        order_item.total_price += (product_item.price * self.quantity)
        order_item.total_delivery_fee += product_item.delivery_fee
        order_item.save()


    def delete(self):
        order_item = Order.objects.get(pk=self.order.pk)
        product_item = Product.objects.get(pk=self.product.pk)
        order_item.total_price -= (product_item.price * self.quantity)
        order_item.total_delivery_fee -= product_item.delivery_fee
        order_item.save()
        super().delete()
