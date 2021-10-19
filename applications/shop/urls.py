from rest_framework.routers import SimpleRouter

from applications.shop.views import ProductViewSet, CategoryViewSet


router = SimpleRouter()

router.register('products', ProductViewSet)
router.register('category', CategoryViewSet)
# router.register('order', OrderViewSet)

urlpatterns = []

urlpatterns += router.urls