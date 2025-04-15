# usueria/urls.py

from django.urls import path
from .views import CrearAlmacenView,CrearCategoriaView,CrearMarcaView ,CrearProductoView ,CrearMercaderiaView
from .controllers.controllers_categorias import obtenerAlmacen,obtenerCategoria,obtenerMarca, actualizar_marca

urlpatterns = [
    path('/marca', CrearMarcaView.as_view(), name='marca'),
    path('/categoria',CrearCategoriaView.as_view(), name='categoria' ),
    path('/almacen',CrearAlmacenView.as_view(), name='almacen' ),
    path('producto/',CrearProductoView.as_view(), name='producto' ),
    path('mercaderia/crear/', CrearMercaderiaView.as_view(), name='crear-mercaderia'),
    
    path('/obtener-marca', obtenerMarca, name='obtener-marca'),
    path('/obtener-almacen', obtenerAlmacen, name='obtener-almacen'),
    path('/obtener-categoria', obtenerCategoria, name='obtener-categoria'),
    
    path('/actualizar-marca', actualizar_marca),
]
