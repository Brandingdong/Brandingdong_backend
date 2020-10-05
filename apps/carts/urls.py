from rest_framework.routers import SimpleRouter

from carts.views import CartViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', CartViewSet)

urlpatterns = router.urls
