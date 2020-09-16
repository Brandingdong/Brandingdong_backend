from django.contrib.auth import get_user_model
from rest_framework import serializers

from carts.models import Cart, CartItem
from products.serializers import ProductSerializer

User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ('products', 'quantity', 'sub_total')


class CartSerializer(serializers.ModelSerializer):
    user = User
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('user', 'items', 'total_price')
