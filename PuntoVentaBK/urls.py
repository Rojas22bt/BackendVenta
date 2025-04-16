
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Otras rutas de tus apps
    path('api/usuario', include('userrs.urls')),
    path('api/inventario', include('inventario.urls')),
    path('api/', include('venta.urls')),
    # URLs para JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/usuario', include('userrs.urls')),
#     path('api/inventario', include('inventario.urls')),
#     path('api/', include('venta.urls')),
# ]
