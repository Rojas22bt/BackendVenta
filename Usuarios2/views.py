from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Bitacora
from .serializers import UsuarioRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

class Register(APIView):
    def post(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({"mensaje": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        contraseña = request.data.get("contraseña")
        user = authenticate(request, correo=correo, password=contraseña)

        if user is not None:
            login(request, user)
            Bitacora.objects.create(usuario=user, accion="Inicio de sesión", ip=get_client_ip(request))
            refresh = RefreshToken.for_user(user)
            return Response({
                "mensaje": "Login exitoso",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    def post(self, request):
        user = request.user
        Bitacora.objects.create(usuario=user, accion="Cierre de sesión", ip=get_client_ip(request))
        logout(request)
        return Response({"mensaje": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
