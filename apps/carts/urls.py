from rest_framework.routers import SimpleRouter

from carts.views import CartViewSet, CartItemsViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'cart', CartViewSet)
router.register(r'items', CartItemsViewSet)

urlpatterns = router.urls
