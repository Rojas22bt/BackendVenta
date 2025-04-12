from rest_framework import serializers
from BaseDatos.models import Rol, Usuario, Documento, DetalleDocumento

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

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

