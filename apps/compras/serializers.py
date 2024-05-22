from rest_framework import serializers
from .models import Cart, CartItem
from apps.productos.serializers import ProductoSerializer  # Importa el serializador de Producto desde la aplicación productos

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductoSerializer()  # Usa el serializador de Producto para representar el producto

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # Usa el serializador de CartItem para representar los ítems del carrito

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'precio_total', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cart = Cart.objects.create(**validated_data)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        cart.update_total()
        return cart