from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MetodoPagoSerializers, OfertasSerializers , FacturaVentaSerializer

class CrearMetodPagoView(APIView):
    def post(self,request):
        serializer = MetodoPagoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje":"Metodo de Pago creado exitosamente",
                "data":serializer.data
            },status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOfertaView(APIView):
    def post(self,request):
        serializer = OfertasSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Oferta agregada",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class createFacturaView(APIView):
    def post(self, request):
        serializer = FacturaVentaSerializer(data=request.data)
        if serializer.is_valid():
            resultado = serializer.save()
            return Response({
                "mensaje": "Venta exitosa",
                "data": resultado  # ← aquí se usa el diccionario retornado desde create()
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)