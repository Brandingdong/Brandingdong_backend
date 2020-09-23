from django.contrib.auth import get_user_model
from rest_framework import serializers

from orders.models import Order

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    user = User

    class Meta:
        model = Order
        fields = ('user', 'receiver', 'address1', 'address2', 'phoneNum', 'orderDate', 'totalPrice', 'message')
