from rest_framework.response import Response
from rest_framework.decorators import api_view
from BaseDatos.models import Bitacora
from .serializers import BitacoraSerializer

@api_view(['GET'])
def obtenerBitacora(request):
    bitacoras = Bitacora.objects.all()
    serializer = BitacoraSerializer(bitacoras, many=True)
    return Response(serializer.data)
    
        