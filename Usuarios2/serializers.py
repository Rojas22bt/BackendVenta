from rest_framework import serializers
from .models import Usuario, Cliente
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    contraseña = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo', 'telefono', 'fecha_nacimiento', 'sexo', 'estado', 'contraseña']
        extra_kwargs = {
            'contraseña': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('contraseña')  # usamos 'contraseña' recibido
        usuario = Usuario(**validated_data)
        usuario.set_password(password)  # lo convertimos a hash correctamente
        usuario.save()
        return usuario

class ClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Cliente
        fields = ['usuario', 'puntos']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        password = usuario_data.pop('contraseña')  # ajustamos aquí también
        usuario = Usuario(**usuario_data)
        usuario.set_password(password)
        usuario.save()
        cliente = Cliente.objects.create(usuario=usuario, **validated_data)
        return cliente

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Puedes agregar campos personalizados al token si quieres
        token['nombre'] = user.nombre
        token['correo'] = user.correo

        return token

    def validate(self, attrs):
        # Cambia 'username' por 'correo'
        attrs['username'] = attrs.get('correo')
        return super().validate(attrs)