from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=32)


class SubCategory(models.Model):
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=32)


class Brand(models.Model):
    brand = models.CharField(max_length=32)


class Product(models.Model):
    DELIVERY_CHOICES = [
        ('1', 'OneDayDelivery'),
        ('1', 'OneDayDelivery'),
        ('2', 'RegularDelivery'),
    ]
    SALE_STATUS = [
        ('1', 'ForSale'),
        ('2', 'StopSale'),
        ('3', 'SoldOut'),
    ]

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    registered_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=1, choices=DELIVERY_CHOICES, blank=True)
    status = models.CharField(max_length=1, choices=SALE_STATUS, blank=True)
    is_discount = models.BooleanField()
    discount_rate = models.PositiveIntegerField(default=0)


class ProductOption(models.Model):
    SIZE_CHOICES = [
        ('1', 'X-SMALL'),
        ('2', 'SMALL'),
        ('3', 'MEDIUM'),
        ('4', 'LARGE'),
    ]
    COLOR_CHOICES = [
        ('1', 'WHITE'),
        ('2', 'BLACK'),
        ('3', 'GRAY'),
        ('4', 'RED'),
        ('5', 'BLUE'),
        ('6', 'GREEN'),
        ('7', 'YELLOW'),
        ('8', 'PURPLE'),
        ('9', 'BROWN'),
        ('10', 'etc'),
    ]
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES, blank=True)
    color = models.CharField(max_length=2, choices=COLOR_CHOICES, blank=True)


class ProductInfo(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', verbose_name='상품이미지')
    detail = models.TextField(blank=True)
    info = models.TextField(blank=True)
