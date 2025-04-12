# usueria/urls.py

from django.urls import path
from .views import CrearAlmacenView,CrearCategoriaView,CrearMarcaView

urlpatterns = [
    path('marca/', CrearMarcaView.as_view(), name='marca'),
    path('categoria/',CrearCategoriaView.as_view(), name='categoria' ),
    path('almacen/',CrearAlmacenView.as_view(), name='almacen' ),

]
