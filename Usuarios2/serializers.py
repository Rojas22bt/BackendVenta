from rest_framework import serializers
from .models import Usuario

class UsuarioRegisterSerializer(serializers.ModelSerializer):
    contraseña = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contraseña']

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
