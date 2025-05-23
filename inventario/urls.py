# usueria/urls.py

from django.urls import path
from .views import CrearAlmacenView,CrearCategoriaView,CrearMarcaView ,CrearProductoView ,CrearMercaderiaView
from .controllers.controllers_categorias import obtenerAlmacen,obtenerCategoria,obtenerMarca, actualizar_marca, actualizar_almacen,actualizar_categoria
from .controllers.controllers_producto import obtenerProductos, actualizar_producto, obtenerProductosActivos

urlpatterns = [
    path('/marca', CrearMarcaView.as_view(), name='marca'),
    path('/categoria',CrearCategoriaView.as_view(), name='categoria' ),
    path('/almacen',CrearAlmacenView.as_view(), name='almacen' ),
    path('/producto',CrearProductoView.as_view(), name='producto' ),
    path('/mercaderia/crear', CrearMercaderiaView.as_view(), name='crear-mercaderia'),
    
    path('/obtener-marca', obtenerMarca, name='obtener-marca'),
    path('/obtener-almacen', obtenerAlmacen, name='obtener-almacen'),
    path('/obtener-categoria', obtenerCategoria, name='obtener-categoria'),
    
    path('/actualizar-marca', actualizar_marca),
    path('/actualizar-categoria', actualizar_categoria),
    path('/actualizar-almacen', actualizar_almacen),
    
    path('/obtener-producto',obtenerProductos,name='obtener-productos'),
    path('/actualizar-producto',actualizar_producto),
    path('/obtener-productos-activos',obtenerProductosActivos, name='obtenerActivos'),
]
