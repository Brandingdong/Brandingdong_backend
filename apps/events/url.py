from rest_framework import routers

from events import apis

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', apis.EventsViewSet)

urlpatterns = router.urls