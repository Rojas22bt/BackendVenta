from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from BaseDatos.models import Producto
from .serializers import ProductoSerializer


@api_view(['GET'])
def obtenerProductos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtenerProductosActivos(request):
    productos = Producto.objects.filter(estado=True, stock__gt=0)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def actualizar_producto(request):
    id_producto = request.data.get('id')
    if not id_producto:
        return Response({'error': 'El id es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        producto = Producto.objects.get(id=id_producto)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Producto actualizado correctamente",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 