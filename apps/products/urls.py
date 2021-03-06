from rest_framework import routers

from products import views

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'detail', views.ProductViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'subcategory', views.SubCategoryViewSet)
router.register(r'brand', views.BrandViewSet)
router.register(r'option', views.ProductOptionViewSet)
router.register(r'images', views.ProductImageViewSet)
router.register(r'info_image', views.ProductInfoImageViewSet)
router.register(r'info', views.ProductInfoViewSet)
router.register(r'sell_info', views.SellingInfoViewSet)


urlpatterns = router.urls
