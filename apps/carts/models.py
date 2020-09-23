from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()

    def total_price(self):
        total = CartItem.objects.filter(cart=self).annotate(total_price=sum('sub_total'))

        return total


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='items', on_delete=models.CASCADE)
    products = models.ForeignKey('products.Product', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.PositiveIntegerField()

    def sub_total(self):
        return self.goods.price * self.quantity

