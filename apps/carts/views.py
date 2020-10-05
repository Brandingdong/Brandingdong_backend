from django.contrib.auth import get_user_model
from rest_framework import viewsets

from carts.models import Cart, CartItems
from carts.serializers import CartSerializer, CartItemsSerializer

User = get_user_model()


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().prefetch_related('cart_items')
    serializer_class = CartSerializer


class CartItemsViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all().select_related('product', 'option')
    serializer_class = CartItemsSerializer
