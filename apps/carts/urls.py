from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from carts.views import CartViewSet, CartItemViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', CartViewSet)

cart_router = NestedSimpleRouter(router, '', lookup='cart')
cart_router.register(r'items', CartItemViewSet)

urlpatterns = router.urls

