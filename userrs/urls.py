# usueria/urls.py

from django.urls import path
from .views import CrearRolView

urlpatterns = [
    path('rol/', CrearRolView.as_view(), name='crear_rol'),
]
