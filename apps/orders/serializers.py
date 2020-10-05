import time
from random import Random

from django.contrib.auth import get_user_model
from rest_framework import serializers

from orders.models import OrderItems, Order
from products.serializers import ProductSerializer, ProductOptionSerializer

User = get_user_model()


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    option = ProductOptionSerializer()

    class Meta:
        model = OrderItems
        fields = (
            'product',
            'option',
            'quantity',
        )


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'user',
            'name',
            'phone',
            'email',
            'receiver',
            'receiver_phone',
            'zip_code',
            'destination',
            'detail_destination',
            'delivery_request',
            'order_items',
            'point_use',
            'payment',
            'total_price',
            'total_delivery_fee',
            'final_price',
        )
