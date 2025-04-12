from rest_framework import serializers
from BaseDatos.models import MetodoDePago,Transaccion,Factura,Oferta,NotaVenta,VentaOferta,DetalleOferta,DetalleVenta,Producto

class MetodoPagoSerializers(serializers.ModelSerializer):
    class Meta:
        model = MetodoDePago
        fields = ['id','nombre']
                
class OfertasSerializers(serializers.ModelSerializer):
    productos = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    class Meta:
        model = Oferta
        fields = [
            'id',
            'descripcion',
            'fecha_inicio',
            'fecha_final',
            'precio',
            'estado',
            'productos'
        ]
    
    def create(self,validated_data):
        productos_data = validated_data.pop('productos',[])
        oferta = Oferta.objects.create(**validated_data)
        
        for prod in productos_data:
            producto = Producto.objects.get(id=prod['id'])
            cantidad = prod['cantidad']

            # Crear el registro en detalleOferta
            DetalleOferta.objects.create(
                oferta = oferta,
                producto=producto,
                cantidad=cantidad,
            )

        return oferta
    
class FacturaVentaSerializers(serializers.Serializer):
    nit = serializers.IntegerField()
    descripcion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fecha = serializers.DateField()
    precio_unidad = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    cod_autorizacion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    estado = serializers.BooleanField(default=True)

    detalle = serializers.CharField()  # para la transacción
    metodo_pago = serializers.IntegerField()  # ID de método de pago

    usuario = serializers.IntegerField()  # ID del usuario

    productos = serializers.ListField(
        child=serializers.DictField(), required=False
    )
    ofertas = serializers.ListField(
        child=serializers.DictField(), required=False
    )

    def create(self, validated_data):
        productos_data = validated_data.pop('productos', [])
        ofertas_data = validated_data.pop('ofertas', [])

        # 1. Crear la transacción
        metodo_pago_id = validated_data.pop('metodo_pago')
        transaccion = Transaccion.objects.create(
            detalle=validated_data.pop('detalle'),
            metodo_pago_id=metodo_pago_id
        )

        # 2. Crear la factura
        factura = Factura.objects.create(**validated_data)

        # 3. Crear la nota de venta
        nota_venta = NotaVenta.objects.create(
            descripcion="Venta registrada",
            transaccion=transaccion,
            factura=factura,
            usuario_id=validated_data.pop('usuario')
        )

        # 4. Crear detalle de venta para productos
        for prod in productos_data:
            producto_id = prod.get('id')
            cantidad = prod.get('cantidad', 1)

            if producto_id:
                producto = Producto.objects.get(id=producto_id)

                if producto.stock < cantidad:
                    raise serializers.ValidationError(
                        f"Stock insuficiente para el producto '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {cantidad}"
                    )
                DetalleVenta.objects.create(
                    producto=producto,
                    nota_venta=nota_venta,
                    cantidad=cantidad
                )
                producto.stock -= cantidad
                producto.save()

        # 5. Crear venta oferta para ofertas
        for oferta in ofertas_data:
            oferta_id = oferta.get('id')
            cantidad = oferta.get('cantidad', 1)
            if oferta_id:
                VentaOferta.objects.create(
                    oferta_id=oferta_id,
                    nota_venta=nota_venta,
                    cantidad=cantidad
                )

        return {
            "factura_id": factura.id,
            "nota_venta_id": nota_venta.id,
            "transaccion_id": transaccion.id
        }