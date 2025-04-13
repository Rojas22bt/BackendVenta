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
    
class FacturaVentaSerializer(serializers.Serializer):
    factura = serializers.DictField()
    transaccion = serializers.DictField()
    nota_venta = serializers.DictField()
    productos = serializers.ListField(child=serializers.DictField(), required=False)
    ofertas = serializers.ListField(child=serializers.DictField(), required=False)

    def create(self, validated_data):
        factura_data = validated_data.pop("factura")
        transaccion_data = validated_data.pop("transaccion")
        nota_venta_data = validated_data.pop("nota_venta")
        productos_data = validated_data.pop("productos", [])
        ofertas_data = validated_data.pop("ofertas", [])

        # 1. Crear la transacción
        transaccion = Transaccion.objects.create(
            detalle=transaccion_data["detalle"],
            metodo_pago_id=transaccion_data["metodo_pago"]
        )

        # 2. Crear la factura
        factura = Factura.objects.create(**factura_data)

        # 3. Crear la nota de venta
        nota_venta = NotaVenta.objects.create(
            descripcion=nota_venta_data["descripcion"],
            transaccion=transaccion,
            factura=factura,
            usuario_id=nota_venta_data["usuario"]
        )

        # 4. Crear detalle de venta para productos
        for prod in productos_data:
            producto = Producto.objects.get(id=prod["id"])
            cantidad = prod.get("cantidad", 1)

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
            VentaOferta.objects.create(
                oferta_id=oferta["id"],
                nota_venta=nota_venta,
                cantidad=oferta.get("cantidad", 1)
            )

        return {
            "factura_id": factura.id,
            "nota_venta_id": nota_venta.id,
            "transaccion_id": transaccion.id
        }