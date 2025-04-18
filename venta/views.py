from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .controllers.serializers import MetodoPagoSerializers, OfertasSerializers , FacturaVentaSerializer
from django.conf import settings
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@api_view(['POST'])
def crear_pago(request):
    try:
        data = request.data
        amount = int(float(data.get("amount", 0)) * 100)  # convertir a centavos
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=["card"],
        )
        return Response({"clientSecret": intent.client_secret})
    except Exception as e:
        return Response({"error": str(e)}, status=400)

class CrearMetodPagoView(APIView):
    def post(self,request):
        serializer = MetodoPagoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje":"Metodo de Pago creado exitosamente",
                "data":serializer.data
            },status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOfertaView(APIView):
    def post(self,request):
        serializer = OfertasSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "mensaje": "Oferta agregada",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class createFacturaView(APIView):
    def post(self, request):
        serializer = FacturaVentaSerializer(data=request.data)
        if serializer.is_valid():
            resultado = serializer.save()
            return Response({
                "mensaje": "Venta exitosa",
                "data": resultado  # ← aquí se usa el diccionario retornado desde create()
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)