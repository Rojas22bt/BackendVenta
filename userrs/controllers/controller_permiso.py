from rest_framework.response import Response
from rest_framework.decorators import api_view
from BaseDatos.models import Permiso
from .serializers import PermisoSerializer

@api_view(['GET'])
def obtnerPermisos(request):
    permisos = Permiso.objects.all()
    serializer = PermisoSerializer(permisos, many=True)
    return Response(serializer.data)


    