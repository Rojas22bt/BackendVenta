from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from BaseDatos.models import Permiso
from rest_framework import status
from .serializers import PermisoSerializer

@api_view(['GET'])
def obtnerPermisos(request):
    permisos = Permiso.objects.all()
    serializer = PermisoSerializer(permisos, many=True)
    return Response(serializer.data)


class ActualizarPermisosAPIView(APIView):
    def post(self, request):
        rol_id = request.data.get("rolActualizo")
        permisos = request.data.get("permisos", [])

        if not rol_id or not isinstance(permisos, list):
            return Response({"error": "Datos inválidos"}, status=status.HTTP_400_BAD_REQUEST)

        errores = []

        for p in permisos:
            permiso_id = p.get("id")
            nuevo_estado = p.get("estado")

            try:
                permiso = Permiso.objects.get(id=permiso_id, rol_id=rol_id)
                permiso.estado = nuevo_estado
                permiso.save()
            except Permiso.DoesNotExist:
                errores.append(permiso_id)

        if errores:
            return Response({
                "mensaje": "Algunos permisos no fueron encontrados para el rol especificado.",
                "errores": errores
            }, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response({"mensaje": "Permisos actualizados correctamente"}, status=status.HTTP_200_OK)
