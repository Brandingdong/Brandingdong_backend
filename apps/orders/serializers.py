import time
from random import Random

from django.contrib.auth import get_user_model
from rest_framework import serializers

from orders.models import OrderItem, OrderInfo
from products.serializers import ProductSerializer

User = get_user_model()


class OrderItemsSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderItemsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = User

    order_sn = serializers.CharField(read_only=True)
    order_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr=random_ins.randint(10, 99))

        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
