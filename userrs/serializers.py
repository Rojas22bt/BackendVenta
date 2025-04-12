from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from BaseDatos.models import Rol, Usuario, Documento, DetalleDocumento ,Privilegio,Permiso

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']
        
class PrivilegiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilegio
        fields = ['id','descripcion']

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['id','descripcion']

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    documentos = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'nombre',
            'correo',
            'telefono',
            'fecha_nacimiento',
            'sexo',
            'estado',
            'password',
            'rol',
            'documentos'
        ]

    def create(self, validated_data):
        documentos_data = validated_data.pop('documentos',[])
        password = validated_data.pop("password")
        rol = validated_data.pop("rol")  # Esto llega como una instancia o ID

        usuario = Usuario.objects.create_user(
            password=password,
            rol=rol,  # puede ser ID o instancia
            **validated_data
        )
        
        for doc in documentos_data:
            DetalleDocumento.objects.create(
                usuario=usuario,
                documento_id = doc.get('id'),
                numero=doc.get('numero')
            )
            
        
        
        return usuario

class UsuarioLoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self,data):
        correo = data.get('correo')
        password = data.get('password')
        
        usuario = authenticate(username=correo, password=password)
        if usuario is None:
            raise serializers.ValidationError("Crendenciales no validas")
        if not usuario.estado:
            raise serializers.ValidationError("Usuario inactivo")
        
        refresh = RefreshToken.for_user(usuario)
        
        documentos = DetalleDocumento.objects.filter( usuario=usuario).vaues(
            'documento__descripcion','numero'
        )
        
        permisos = Permiso.objects.filter(rol=usuario.rol, estado=True).values_list(
            'privilegio__descripcion', flat=True
        )
        
        return {
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "telefono": usuario.telefono,
                "fecha_nacimiento": usuario.fecha_nacimiento,
                "sexo": usuario.sexo,
                "rol": usuario.rol.nombre,
                "permisos": list(permisos),
                "documentos": list(documentos)
            }
        }
        
