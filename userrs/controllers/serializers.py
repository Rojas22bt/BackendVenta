from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from BaseDatos.models import Rol, Usuario, Documento, DetalleDocumento ,Privilegio,Permiso, Bitacora

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
        
        documentos = DetalleDocumento.objects.filter( usuario=usuario).values(
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
                "puntos":usuario.cliente.puntos,
                "rol": usuario.rol.nombre,
                "permisos": list(permisos),
                "documentos": list(documentos)
            }
        }
        
class BitacoraSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre',read_only=True)
    usuario_correo = serializers.CharField(source='usuario.correo',read_only=True)
    class Meta:
        model = Bitacora
        fields = ['id', 'ip', 'fecha', 'hora', 'accion', 'usuario', 'usuario_nombre','usuario_correo']
        
class UsuarioSerializer(serializers.ModelSerializer):
    cliente_punto = serializers.CharField(source='cliente.puntos',read_only=True)
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
            'rol',
            'cliente_punto']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'
        
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    puntos = serializers.IntegerField(source='cliente.puntos', read_only=True)
    documentos = serializers.SerializerMethodField()

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
            'rol',
            'puntos',
            'documentos'
        ]

    def get_documentos(self, obj):
        return [
            {
                "id": doc.documento_id,  # o doc.id según tu modelo
                "numero": doc.numero
            }
            for doc in obj.detalledocumento_set.all()
        ]