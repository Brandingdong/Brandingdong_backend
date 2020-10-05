from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product, ProductOption

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    total_price = models.PositiveIntegerField(default=0)
    total_delivery_fee = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class CartItems(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='카트', related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cart_item = Cart.objects.get(pk=self.cart.pk)
        product_item = Product.objects.get(pk=self.product.pk)
        cart_item.total_price += (product_item.price * self.quantity)
        cart_item.total_delivery_fee += product_item.delivery_fee
        cart_item.save()


    def delete(self):
        cart_item = Cart.objects.get(pk=self.cart.pk)
        product_item = Product.objects.get(pk=self.product.pk)
        cart_item.total_price -= (product_item.price * self.quantity)
        cart_item.total_delivery_fee -= product_item.delivery_fee
        cart_item.save()
        super().delete()
