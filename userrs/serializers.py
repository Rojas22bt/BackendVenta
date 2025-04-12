from rest_framework import serializers
from BaseDatos.models import Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']