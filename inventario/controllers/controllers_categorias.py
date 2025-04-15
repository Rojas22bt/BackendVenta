from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
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


@api_view(['PATCH'])
def actualizar_marca(request):
    id_marca = request.data.get('id')
    nuevo_nombre = request.data.get('nombre')

    if not id_marca:
        return Response({'error': 'El id es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
    if not nuevo_nombre:
        return Response({'error': 'El nombre es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        marca = Marca.objects.get(id=id_marca)
    except Marca.DoesNotExist:
        return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    marca.nombre = nuevo_nombre
    marca.save()

    return Response({
        'mensaje': f"Marca '{marca.nombre}' actualizada correctamente ✅"
    }, status=status.HTTP_200_OK)
        
        
