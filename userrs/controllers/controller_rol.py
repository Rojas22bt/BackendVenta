from rest_framework.response import Response
from rest_framework.decorators import api_view
from BaseDatos.models import Rol
from .serializers import RolSerializer



@api_view(['GET'])
def obtenerRol(request):
    roles = Rol.objects.all()
    serializer = RolSerializer(roles, many=True)
    return Response(serializer.data)

    
        

