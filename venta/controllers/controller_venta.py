from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from datetime import datetime

from BaseDatos.models import Usuario, NotaVenta, DetalleVenta, VentaOferta


class ComprobanteView(APIView):
    def post(self, request):
        correo = request.data.get("correo")
        fecha_inicio = request.data.get("fecha_inicio")
        fecha_fin = request.data.get("fecha_fin")

        if not correo or not fecha_inicio or not fecha_fin:
            return Response({"error": "Se requieren correo, fecha_inicio y fecha_fin"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(correo=correo)

            notas = NotaVenta.objects.filter(
                usuario=usuario,
                factura__fecha__range=[fecha_inicio, fecha_fin]
            ).prefetch_related(
                Prefetch('detalleventa_set', queryset=DetalleVenta.objects.select_related('producto')),
                Prefetch('ventaoferta_set', queryset=VentaOferta.objects.select_related('oferta')),
                'factura'
            )

            comprobantes = []
            for nota in notas:
                factura = nota.factura
                detalles_productos = [{
                    "producto": detalle.producto.nombre,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": float(detalle.producto.precio),
                    "subtotal": float(detalle.cantidad * detalle.producto.precio)
                } for detalle in nota.detalleventa_set.all()]

                detalles_ofertas = [{
                    "oferta": vo.oferta.descripcion,
                    "cantidad": vo.cantidad,
                    "precio_oferta": float(vo.oferta.precio),
                    "subtotal": float(vo.cantidad * vo.oferta.precio)
                } for vo in nota.ventaoferta_set.all()]

                comprobantes.append({
                    "factura_id": factura.id,
                    "fecha": factura.fecha,
                    "descripcion": factura.descripcion,
                    "cod_autorizacion": factura.cod_autorizacion,
                    "precio_total": float(factura.precio_total),
                    "detalles_productos": detalles_productos,
                    "detalles_ofertas": detalles_ofertas
                })

            return Response({
                "cliente_id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "comprobantes": comprobantes
            }, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
