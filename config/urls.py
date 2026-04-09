from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Panel de Administración
    path('admin/', admin.site.urls),

    # 2. Rutas de la aplicación 'products' (catálogo, CRUD, carrito, auth)
    path('', include('products.urls')),

    # 3. Rutas específicas del proyecto principal
    # La ruta raíz (/) es manejada por una vista que redirige al catálogo principal
    path('', views.catalog, name='catalog'),
    # La ruta de checkout se mantiene aquí porque su vista está en config/views.py
    path('checkout/', views.checkout, name='checkout'),
]

# Configuración para servir archivos de media (imágenes subidas) en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)