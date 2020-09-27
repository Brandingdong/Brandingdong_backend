from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    items = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    add_time = models.DateTimeField(default=datetime.now)
