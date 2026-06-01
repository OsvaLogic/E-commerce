from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/api/products/', permanent=True)), # Redirige la raíz a la API
    path('', include('products.urls')), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Endpoint de Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refrescar Token
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
