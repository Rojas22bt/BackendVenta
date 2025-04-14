# usueria/urls.py

from django.urls import path
from .views import CrearRolView, RegistrarUsuarioViem,CrearDocumentoViem,CrearPrivilegioViem , LoginUsuarioView

from .controllers.controller_bitacora import obtenerBitacora
from .controllers.controlles_usuario import obtenerUsuarios

urlpatterns = [
    path('rol/', CrearRolView.as_view(), name='crear_rol'),
    path('/registro',RegistrarUsuarioViem.as_view(), name='usuario-registro' ),
    path('documento/',CrearDocumentoViem.as_view(), name='documento-registro' ),
    path('privilegio/',CrearPrivilegioViem.as_view(), name='privilegio-registro' ),
    path('/login',LoginUsuarioView.as_view(), name='login' ),
    
    
    path('/bitacora', obtenerBitacora, name="get_bitacoras"),
    path('/',obtenerUsuarios,name='obtener-usuarios')
    
]
