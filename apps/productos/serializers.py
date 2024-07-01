from rest_framework import serializers
from .models import Producto, Precio

class PrecioSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(required=False)
    valor = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Precio
        fields = ('fecha', 'valor')

class ProductoSerializer(serializers.ModelSerializer):
    precio = PrecioSerializer(many=True, required=False)  # precio no requerido

    class Meta:
        model = Producto
        fields = ('codigo_producto', 'marca', 'modelo', 'codigo', 'nombre', 'stock', 'precio')

    def create(self, validated_data):
        precios_data = validated_data.pop('precio', [])  # Usar lista vacía si no hay precios
    
        producto = Producto.objects.create(**validated_data)

        for precio_data in precios_data:
            Precio.objects.create(producto=producto, **precio_data)

        return producto
