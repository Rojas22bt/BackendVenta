from django.urls import path
from .views import CrearMetodPagoView, CreateOfertaView, createFacturaView

urlpatterns = [
    path('venta/metodoPago/', CrearMetodPagoView.as_view(), name='crear-pago'),
    path('/oferta/register', CreateOfertaView.as_view(), name='crear-pago'),
    path('venta/factura/', createFacturaView.as_view(), name='factura-venta'),
    
]
