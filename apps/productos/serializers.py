from rest_framework import serializers
from .models import Producto, Precio

class PrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precio
        fields = ('fecha', 'valor')

class ProductoSerializer(serializers.ModelSerializer):
    precio = PrecioSerializer(many=True, read_only=True) 

    class Meta:
        model = Producto
        fields = ('codigo_producto', 'marca', 'modelo', 'codigo', 'nombre', 'stock', 'precio')

    def create(self, validated_data):
        precios_data = validated_data.pop('precio', [])  

       
        producto = Producto.objects.create(**validated_data)

       
        for precio_data in precios_data:
            Precio.objects.create(producto=producto, **precio_data)

        return producto


