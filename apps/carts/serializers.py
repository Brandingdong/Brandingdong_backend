from django.contrib.auth import get_user_model
from rest_framework import serializers

from carts.models import Cart, CartItems
from products.models import Product
from products.serializers import ProductSerializer, ProductOptionSerializer

User = get_user_model()


class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    option = ProductOptionSerializer()

    class Meta:
        model = CartItems
        fields = (
            'product',
            'option',
            'quantity',
        )
        read_only_fields = (
            'product',
            'option',
        )


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            'user',
            'cart_items',
            'total_price',
            'total_delivery_fee',
        )