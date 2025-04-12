from BaseDatos.models import Marca, Categoria, Almacen , Producto, IngresoProducto, Mercaderia
from rest_framework import serializers

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id','nombre']
    
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nombre']
        
class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ['id','descripcion','cantidad']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id',
            'nombre',
            'modelo',
            'stock',
            'precio',
            'estado',
            'almacen',
            'categoria',
            'marca'
            ]
    
from rest_framework import serializers
from BaseDatos.models import Mercaderia, IngresoProducto, Producto

class MercaderiaSerializer(serializers.ModelSerializer):
    productos = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    class Meta:
        model = Mercaderia
        fields = [  
            'id',
            'nro_factura',
            'fecha',
            'detalle',
            'cod_autorizacion',
            'estado',
            'productos'
        ]

    def create(self, validated_data):
        productos_data = validated_data.pop('productos', [])
        mercaderia = Mercaderia.objects.create(**validated_data)

        for prod in productos_data:
            producto = Producto.objects.get(id=prod['producto'])
            cantidad = prod['cantidad']
            precio_compra = prod['precio_compra']

            # Crear el registro en IngresoProducto
            IngresoProducto.objects.create(
                mercaderia=mercaderia,
                producto=producto,
                cantidad=cantidad,
                precio_compra=precio_compra
            )

            # Actualizar el stock del producto
            producto.stock += cantidad
            producto.save()

        return mercaderia
