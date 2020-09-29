from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from carts.models import Cart
from carts.serializers import CartSerializer, CartDetailSerializer

User = get_user_model()


class CartViewSet(viewsets.ModelViewSet):
    """
    list： 카트 아이템 조회
    create: 카트 아이템 생성
    delete: 카트 아이템 삭제
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    PermissionError = [permissions.AllowAny]
    lookup_field = "items_id"

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        items = shop_cart.items
        items.options.stock -= shop_cart.quantity
        items.save()

    def perform_destroy(self, instance):
        items = instance.items
        items.options.stock += instance.quantity
        items.save()
        instance.delete()

    def perform_update(self, serializer):
        cart_existed = Cart.objects.get(id=serializer.instance.id)
        cart_quantity = cart_existed.quantity
        saved_record = serializer.save()

        quantity = saved_record.nums - cart_quantity
        items = saved_record.items
        items.option.stock -= quantity
        items.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return CartDetailSerializer
        else:
            return CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)