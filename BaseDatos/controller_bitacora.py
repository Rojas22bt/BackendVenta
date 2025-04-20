from .models import Bitacora

def registrar_bitacora(request, accion, usuario=None):
    Bitacora.objects.create(
        ip=request.META.get('REMOTE_ADDR', '0.0.0.0'),
        accion=accion,
        usuario=usuario
    )