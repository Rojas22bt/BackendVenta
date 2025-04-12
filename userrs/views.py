# usueria/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from BaseDatos.models import Rol
from .serializers import RolSerializer

class CrearRolView(APIView):
    def post(self, request):
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Rol creado con éxito", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
