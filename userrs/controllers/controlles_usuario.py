from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from BaseDatos.models import Usuario, Rol, DetalleDocumento, Calificacion, Comentario
from .serializers import UsuarioSerializer, PerfilUsuarioSerializer, CalificacionResponseSerializer, ComentarioSerializer

@api_view(['GET'])
def obtenerUsuarios(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)
    
    
class crearCalificacion(APIView):
    def post(self, request):
        serializer = CalificacionResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Gracias por tu Calificacion", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class crerComentario(APIView):
    def post(self, request):
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Gracias por el comentario", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
      
@api_view(['GET'])
def obtenerComentario(request):
    comentario = Comentario.objects.all()
    serializer = ComentarioSerializer(comentario, many=True)
    return Response(serializer.data)
    
    
    
@api_view(['GET'])
def obtenerCalificacion(request):
    calificacion = Calificacion.objects.all()
    serializer = CalificacionResponseSerializer(calificacion, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtenerPerfil(request):
    usuarios = Usuario.objects.all()
    serializer = PerfilUsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)
        
@api_view(['PATCH'])
def actualizar_usuario(request):
    id_usuario = request.data.get('id')
    if not id_usuario:
        return Response({'error': 'El id es obligatorio para encontrar al usuario'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuarios = Usuario.objects.get(id=id_usuario)
    except Usuario.DoesNotExist:
         return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
     
    campos_actualizados = []
    
    if 'nombre' in request.data:
        usuarios.nombre = request.data['nombre']
        campos_actualizados.append('nombre')
    
    if 'telefono' in request.data:
        usuarios.telefono = request.data['telefono']
        campos_actualizados.append('telefono')

    if 'fecha_nacimiento' in request.data:
        usuarios.fecha_nacimiento = request.data['fecha_nacimiento']
        campos_actualizados.append('fecha_nacimiento')

    if 'sexo' in request.data:
        usuarios.sexo = request.data['sexo']
        campos_actualizados.append('sexo')

    if 'estado' in request.data:
        usuarios.estado = request.data['estado']
        campos_actualizados.append('estado')

    if 'rol' in request.data:
        try:
            nuevo_rol = Rol.objects.get(id=request.data['rol'])
            usuarios.rol = nuevo_rol
            campos_actualizados.append('rol')
        except Rol.DoesNotExist:
            return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    usuarios.save()

    return Response({
        'mensaje': f"Usuario '{usuarios.nombre}' actualizado correctamente ✅",
        'campos_actualizados': campos_actualizados
    })