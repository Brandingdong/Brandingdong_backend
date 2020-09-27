from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class OrderInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True)
    post_script = models.TextField()
    total_amount = models.PositiveIntegerField(default=1)

    address = models.CharField(max_length=100, default="")
    signer_name = models.CharField(max_length=20, default="")
    singer_mobile = models.CharField(max_length=11)

    order_time = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey('orders.OrderInfo', on_delete=models.CASCADE, related_name="items")
    items = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)

