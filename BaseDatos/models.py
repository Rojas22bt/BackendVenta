from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model


# --------- MÓDULOS DE MÉTODOS Y TRANSACCIONES ---------
class MetodoDePago(models.Model):
    nombre = models.CharField(max_length=20)

class Transaccion(models.Model):
    detalle = models.CharField(max_length=50)
    metodo_pago = models.ForeignKey(MetodoDePago, on_delete=models.CASCADE)

# --------- MÓDULO DE FACTURACIÓN Y VENTAS ---------
class Factura(models.Model):
    nit = models.IntegerField()
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    fecha = models.DateField()
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    cod_autorizacion = models.CharField(max_length=35, blank=True, null=True)
    estado = models.BooleanField(default=True)

class NotaVenta(models.Model):
    descripcion = models.CharField(max_length=199)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

# --------- MÓDULO DE MERCADERÍA Y ALMACÉN ---------
class Mercaderia(models.Model):
    nro_factura = models.IntegerField()
    fecha = models.DateField()
    detalle = models.CharField(max_length=100)
    cod_autorizacion = models.CharField(max_length=35, blank=True, null=True)
    estado = models.BooleanField(default=True)

class Almacen(models.Model):
    descripcion = models.CharField(max_length=199)
    cantidad = models.IntegerField()

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

class Producto(models.Model):
    nombre = models.CharField(max_length=25)
    modelo = models.CharField(max_length=25)
    stock = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

class IngresoProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    mercaderia = models.ForeignKey(Mercaderia, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('producto', 'mercaderia')

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    nota_venta = models.ForeignKey(NotaVenta, on_delete=models.CASCADE)

# --------- MÓDULO DE OFERTAS ---------
class Oferta(models.Model):
    descripcion = models.CharField(max_length=100, blank=True)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

class DetalleOferta(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('oferta', 'producto')

class VentaOferta(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    nota_venta = models.ForeignKey(NotaVenta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = ('oferta', 'nota_venta')

# --------- MÓDULO DE ROLES Y PRIVILEGIOS ---------
class Privilegio(models.Model):
    descripcion = models.CharField(max_length=100)

class Rol(models.Model):
    nombre = models.CharField(max_length=100)

class Permiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    privilegio = models.ForeignKey(Privilegio, on_delete=models.CASCADE)
    estado = models.BooleanField()

    class Meta:
        unique_together = ('rol', 'privilegio')

# -------------------- MANAGER --------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo electrónico es obligatorio")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

# -------------------- MODELO USUARIO --------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    telefono = models.BigIntegerField()
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1)
    estado = models.BooleanField(default=True)
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'telefono', 'fecha_nacimiento', 'sexo', 'rol_id']

    objects = UsuarioManager()

    def __str__(self):
        return self.correo

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    puntos = models.IntegerField()

class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)

class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)

# --------- MÓDULO DE CALIFICACIONES ---------
class Calificacion(models.Model):
    numero = models.DecimalField(max_digits=4, decimal_places=2)

class HistorialCalificacion(models.Model):
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calificacion_valor = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = ('calificacion', 'usuario')

# --------- MÓDULO DE BITÁCORA Y DOCUMENTOS ---------
class Documento(models.Model):
    descripcion = models.CharField(max_length=59)

class DetalleDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    numero = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('documento', 'usuario')

class Bitacora(models.Model):
    ip = models.CharField(max_length=15)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100, blank=True, null=True)

