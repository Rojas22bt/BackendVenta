# usueria/urls.py

from django.urls import path
from .views import CrearRolView, RegistrarUsuarioViem

urlpatterns = [
    path('rol/', CrearRolView.as_view(), name='crear_rol'),
    path('registro/',RegistrarUsuarioViem.as_view(), name='usuario-registro' )
]
