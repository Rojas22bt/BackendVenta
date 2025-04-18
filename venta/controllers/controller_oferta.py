from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from BaseDatos.models import Oferta
from .serializers import OfertasSerializers

@api_view(['GET'])
def obtenerOfertas(request):
    ofertas = Oferta.objects.all()
    serializer = OfertasSerializers(ofertas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtenerOfertasActivas(request):
    ofertas = Oferta.objects.filter(estado=True) 
    serializer = OfertasSerializers(ofertas, many=True)
    return Response(serializer.data)
