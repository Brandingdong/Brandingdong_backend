from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product, ProductOption

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class CartItems(models.Model):
    cart = models.ForeignKey('Cart', blank=True, on_delete=models.CASCADE, verbose_name='카트', related_name='cart_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    option = models.ForeignKey('ProductOption', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    total_price = models.PositiveIntegerField(default=0)
    delivery_fee = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_price= total
        super().save(*args, **kwargs)
        total_price =

