from django.urls import path
from .views import CrearMetodPagoView, CreateOfertaView, createFacturaView
from .controllers.controller_oferta import obtenerOfertas, obtenerOfertasActivas

urlpatterns = [
    path('venta/metodoPago/', CrearMetodPagoView.as_view(), name='crear-pago'),
    path('/oferta/register', CreateOfertaView.as_view(), name='crear-pago'),
    path('venta/factura/', createFacturaView.as_view(), name='factura-venta'),
    
    path('/venta/obtener-ofertas',obtenerOfertas, name='obtener-ofertas'),
    path('/venta/obtener-ofertas-activas',obtenerOfertasActivas, name='obtener-ofertas-activas'),
]
