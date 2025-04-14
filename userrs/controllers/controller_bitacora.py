from rest_framework.response import Response
from BaseDatos.models import Bitacora
from .serializers import BitacoraSerializer

@api_view(['GET'])
def obtener_bitacora(request):
    bitacoras = Bitacora.objects.all()
    serializer = BitacoraSerializer(bitacoras, many=True)
    return Response(serializer.data)
    
        