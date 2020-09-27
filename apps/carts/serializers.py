from django.contrib.auth import get_user_model
from rest_framework import serializers

from carts.models import Cart
from products.models import Product
from products.serializers import ProductSerializer

User = get_user_model()


class CartDetailSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Cart
        fields = ('items', 'quantity')


class CartSerializer(serializers.Serializer):
    user = get_user_model()
    quantity = serializers.IntegerField(default=1, min_value=1,
                                        error_messages={
                                            "min_value": "최소 수량은 1입니다."
                                        })
    items = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        quantity = validated_data["quantity"]
        items = validated_data["items"]

        cart_items = Cart.objects.filter(user=user, items=items)

        if cart_items:
            cart_items = cart_items[0]
            cart_items.quantity += quantity
            cart_items.save()
        else:
            cart_items = Cart.objects.create(**validated_data)

        return cart_items

    def update(self, instance, validated_data):
        instance.quantity = validated_data["quantity"]
        instance.save()
        return instance
