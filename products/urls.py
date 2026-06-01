from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CheckoutAPIView

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('api/products/', include(router.urls)),
    path('api/checkout/', CheckoutAPIView.as_view(), name='api-checkout'),
]
