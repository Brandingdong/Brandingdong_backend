from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer()
    class Meta:
        model = Order
        fields = ('user', 'receiver', 'address1', 'address2', 'phoneNum', 'orderDate', 'totalPrice', 'message')
