# usueria/urls.py

from django.urls import path
from .views import CrearRolView, RegistrarUsuarioViem,CrearDocumentoViem,CrearPrivilegioViem , LoginUsuarioView

from .controllers.controller_bitacora import obtenerBitacora
from .controllers.controlles_usuario import obtenerUsuarios, actualizar_usuario, obtenerPerfil, crearCalificacion, obtenerCalificacion, crerComentario, obtenerComentario
from .controllers.controller_rol import obtenerRol
from .controllers.controller_permiso import obtnerPermisos, ActualizarPermisosAPIView


urlpatterns = [
    path('rol/', CrearRolView.as_view(), name='crear_rol'),
    path('/registro',RegistrarUsuarioViem.as_view(), name='usuario-registro' ),
    path('documento/',CrearDocumentoViem.as_view(), name='documento-registro' ),
    path('privilegio/',CrearPrivilegioViem.as_view(), name='privilegio-registro' ),
    path('/login',LoginUsuarioView.as_view(), name='login' ),
    path('/actualizar-permiso',ActualizarPermisosAPIView.as_view(), name='actualizar-permiso' ),
    path('/calificacion',crearCalificacion.as_view(), name='calificacion' ),
    path('/comentario',crerComentario.as_view(), name='comentario' ),
    
    
    path('/bitacora', obtenerBitacora, name="get_bitacoras"),
    path('/',obtenerUsuarios,name='obtener-usuarios'),
    path('/perfil',obtenerPerfil,name='obtener-perfil'),
    path('/roles',obtenerRol,name='obtener-rol'),
    path('/permisos',obtnerPermisos,name='obtener-permisos'),
    path('/obtener-calificacion',obtenerCalificacion,name='obtener-calificacion'),
    path('/obtener-comentario',obtenerComentario,name='obtener-comentario'),
    

    path('/actualizar',actualizar_usuario),
    
    
]
