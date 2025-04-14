from rest_framework.response import Response
from BaseDatos.models import Bitacora
from .serializers import BitacoraSerializer

def obtener_bitacora(request):
    bitacora = Bitacora.objects.all()
    serializer = BitacoraSerializer(bitacora, may=True)
    return Response(serializer.data)
    
        