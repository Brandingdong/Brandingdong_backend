from rest_framework import mixins, viewsets, permissions

from orders.models import OrderInfo, OrderItem
from orders.serializers import OrderSerializer, OrderDetailSerializer
from carts.models import Cart

class OrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    list : 주문리스트 조회
    retrieve : 주문 상세
    delete : 주문 삭제
    create : 신규 주문 생성
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = Cart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_items = OrderItem()
            order_items.items = shop_cart.items
            order_items.items.quantity = shop_cart.quantity
            order_items.order = order
            order_items.save()

            shop_cart.delete()
        return order
