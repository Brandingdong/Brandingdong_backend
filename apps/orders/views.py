from django.contrib.auth import get_user_model
from rest_framework import viewsets

from orders.models import Order, OrderItems
from orders.serializers import OrderSerializer, OrderItemsSerializer

User = get_user_model()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('order_items')
    serializer_class = OrderSerializer


class CartItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItems.objects.all().select_related('product', 'option')
    serializer_class = OrderItemsSerializer
