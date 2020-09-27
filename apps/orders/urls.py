from rest_framework.routers import SimpleRouter

from orders.views import OrderViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'order', OrderViewSet)

urlpatterns = router.urls
