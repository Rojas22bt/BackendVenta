from rest_framework import generics
from .models import Usuario, Cliente
from .serializers import UsuarioSerializer, ClienteSerializer

class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.select_related('usuario').all()
    serializer_class = ClienteSerializer
