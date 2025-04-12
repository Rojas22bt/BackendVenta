# usueria/urls.py

from django.urls import path
from .views import CrearRolView, RegistrarUsuarioViem,CrearDocumentoViem

urlpatterns = [
    path('rol/', CrearRolView.as_view(), name='crear_rol'),
    path('registro/',RegistrarUsuarioViem.as_view(), name='usuario-registro' ),
    path('documento/',CrearDocumentoViem.as_view(), name='documento-registro' )
]
