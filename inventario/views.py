from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from BaseDatos.models import Marca, Almacen,Categoria
from .serializers import MarcaSerializer, AlmacenSerializer, CategoriaSerializer

class CrearMarcaView(APIView):
    def post(self,request):
        serializer = MarcaSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "mensaje": "Marca registrado exitosamente",
                "data" : serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CrearAlmacenView(APIView):
    def post(self,request):
        serializer = AlmacenSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "mensaje":"Almacen creado exitosamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrearCategoriaView(APIView):
    def post(self,request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "mensaje":"Categoria agregado exitosamente",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

