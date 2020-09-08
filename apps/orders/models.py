from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE)
    goods = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    receiver = models.CharField(max_length=16)
    address1 = models.CharField(max_length=64)
    address2 = models.CharField(max_length=64)
    phoneNum = PhoneNumberField(null=True)
    orderDate = models.DateTimeField(auto_now_add=True)
    totalPrice = models.PositiveIntegerField(default=0)
    message = models.TextField()