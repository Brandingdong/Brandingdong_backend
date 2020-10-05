from rest_framework.routers import SimpleRouter

from orders.views import OrderViewSet, OrderItemsViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'order', OrderViewSet)
router.register(r'items', OrderItemsViewSet)
urlpatterns = router.urls
