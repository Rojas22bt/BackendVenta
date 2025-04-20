from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from BaseDatos.models import Bitacora, Usuario
from rest_framework.views import APIView

from .serializers import BitacoraSerializer

@api_view(['GET'])
def obtenerBitacora(request):
    bitacoras = Bitacora.objects.all()
    serializer = BitacoraSerializer(bitacoras, many=True)
    return Response(serializer.data)
    

class BitacoraCreateAPIView(APIView):
    def post(self, request):
        usuario_id = request.data.get("usuario_id")
        accion = request.data.get("accion")
        if not usuario_id or not accion:
            return Response({"error": "usuario_id y accion son requeridos."},status=400)

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."},status=404)

        Bitacora.objects.create(
            ip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
            accion=accion,
            usuario=usuario
        )

        return Response({"mensaje": "Bitácora registrada correctamente."},status=201)
