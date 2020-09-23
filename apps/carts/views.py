from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from carts.models import Cart, CartItem
from carts.serializers import CartSerializer, CartItemSerializer


class CartViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=True)
    def add(self, request, pk):
        return Response({'success': True})
