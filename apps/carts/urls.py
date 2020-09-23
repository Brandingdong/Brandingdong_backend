from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from carts.views import CartViewSet, CartItemViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'me', CartViewSet)

cart_router = NestedSimpleRouter(router, 'me', lookup='cart')
cart_router.register(r'items', CartItemViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(cart_router.urls)),
]

