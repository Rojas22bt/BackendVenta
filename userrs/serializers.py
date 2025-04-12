from rest_framework import serializers
from BaseDatos.models import Rol, Usuario

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

class UsuarioRegistroSerializer(serializers.ModelSerializer):
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
            'rol'
        ]
    
    def validate_correo(self,value):
        if Usuario.objects.filter(correo=value).exists:
            raise serializers.ValidationError("Este correo ya está registrado")
        return value