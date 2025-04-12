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