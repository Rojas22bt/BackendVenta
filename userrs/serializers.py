from rest_framework import serializers
from BaseDatos.models import Rol, Usuario

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

class UsuarioRegistroSerializer(serializers.ModelSerializer):
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
            'rol'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario.objects.create_user(
            correo=validated_data['correo'],
            password=password,
            **validated_data
        )
        return usuario