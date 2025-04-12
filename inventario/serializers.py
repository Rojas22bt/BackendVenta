from BaseDatos.models import Marca, Categoria, Almacen
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