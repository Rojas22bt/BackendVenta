from rest_framework.response import Response
from rest_framework.decorators import api_view
from BaseDatos.models import Marca,  Almacen, Categoria
from .serializers import MarcaSerializer,CategoriaSerializer,AlmacenSerializer



@api_view(['GET'])
def obtenerMarca(request):
    marcas = Marca.objects.all()
    serializer = MarcaSerializer(marcas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtenerCategoria(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtenerAlmacen(request):
    almacenes = Almacen.objects.all()
    serializer = AlmacenSerializer(almacenes, many=True)
    return Response(serializer.data)

        