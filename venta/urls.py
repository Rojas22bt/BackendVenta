from django.urls import path
from .views import CrearMetodPagoView, CreateOfertaView, createFacturaView, crear_pago
from .controllers.controller_oferta import obtenerOfertas, obtenerOfertasActivas

urlpatterns = [
    path('venta/metodoPago/', CrearMetodPagoView.as_view(), name='crear-pago'),
    path('/oferta/register', CreateOfertaView.as_view(), name='crear-pago'),
    path('/factura', createFacturaView.as_view(), name='factura-venta'),
    path('/crear-pago', crear_pago),
    path('/obtener-ofertas',obtenerOfertas, name='obtener-ofertas'),
    path('/obtener-ofertas-activas',obtenerOfertasActivas, name='obtener-ofertas-activas'),
]
