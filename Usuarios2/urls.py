from django.urls import path
from .views import UsuarioListCreateView, ClienteListCreateView

urlpatterns = [
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
]
