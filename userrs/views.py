# usueria/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from BaseDatos.models import Rol,Usuario,Cliente,Administrador, Bitacora , Documento, DetalleDocumento, Permiso
from .serializers import RolSerializer,UsuarioRegistroSerializer,DocumentoSerializer, PrivilegiosSerializer
from datetime import datetime

class CrearRolView(APIView):
    def post(self, request):
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Rol creado con éxito", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrearDocumentoViem(APIView):
    def post(self, request):
        serializer = DocumentoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Documento creado con éxito","data": serializer.data},status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrarUsuarioViem(APIView):
    def post(self, request):
        serilizer = UsuarioRegistroSerializer(data=request.data)
        if serilizer.is_valid():
            usuario = serilizer.save()
            
            if usuario.rol.id == 2:
                Cliente.objects.create(usuario=usuario, puntos=0)
            elif usuario.rol.id == 1:
                Administrador.objects.create(usuario = usuario)
            
            Bitacora.objects.create(
                ip = request.META.get('REMOTE_ADDR', '0.0.0.0'),
                accion= "Registro de nuevo Usuario",
                usuario=usuario
            )
            
            return Response({
                "mensaje": "Usuario registrado correctamente",
                "usuario": UsuarioRegistroSerializer(usuario).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrearPrivilegioViem(APIView):
    def post(self,request):
        serializer = PrivilegiosSerializer(data = request.data)
        if serializer.is_valid():
            privilegio = serializer.save()
            
            roles = Rol.objects.all()
            
            for rol in roles:
                Permiso.objects.create(
                    privilegio = privilegio,
                    rol=rol,
                    estado=True
                )
                
            return Response({
                "mensaje":"Privilegios creado con permisos asignados a todos los roles",
                "prilegio": PrivilegiosSerializer(privilegio).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)