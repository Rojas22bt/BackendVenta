# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model

# persolanizado para el modelo usuario 
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, contraseña=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, nombre=nombre, **extra_fields)
        usuario.set_password(contraseña)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, contraseña=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(correo, nombre, contraseña, **extra_fields)
    
# modelo usuario segun nuestra base
class  Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    correo= models.EmailField(unique=True)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    genero=models.CharField(
        max_length=20,
        choices=(
            ('M', 'Masculino'),
            ('F', 'Femenino'),
            ('O', 'Otro')
        ),
        null=True, blank=True
    )
    estado=models.BooleanField(default=True)
    direccion=models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']    

    objects = UsuarioManager()

    def _str_(self):
        return self.correo
    
Usuario = get_user_model()

class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)

    def _str_(self):
        return f"{self.usuario} - {self.accion} - {self.fecha} {self.hora}"