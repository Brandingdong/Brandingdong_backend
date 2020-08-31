from rest_framework import routers

from apps.products.views import ProductModelViewSet, CategoryModelViewSet, SubCategoryModelViewSet, BrandModelViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'products', ProductModelViewSet)
router.register(r'category', CategoryModelViewSet)
router.register(r'subcategory', SubCategoryModelViewSet)
router.register(r'brand', BrandModelViewSet)

urlpatterns = router.urls
