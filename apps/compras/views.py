from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.addproductos.models import Cart, CartItem
from apps.productos.models import Producto
import time

@api_view(['POST', 'GET'])
def finalizar_compra(request):
    if request.method == 'GET':
        return Response({'message': 'Debe ingresar el cart_id en el cuerpo de la solicitud POST'}, 
                        status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        cart_id = request.data.get('cart_id')
        if not cart_id:
            return Response({'error': 'Cart ID es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({'error': 'El carrito no existe'}, status=status.HTTP_404_NOT_FOUND)

        # Simulación de proceso de pago
        payment_message = "Trasladando a portal de pago con tarjeta de crédito..."
        print(payment_message)
        time.sleep(5)

        # Actualizar el stock de los productos
        for item in cart.items.all():
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                return Response({'error': f'Stock insuficiente para el producto {product.nombre}'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        # Finalizar la compra eliminando el carrito
        cart.delete()

        # Mensaje final de compra realizada
        time.sleep(5)
        final_message = "Compra realizada!"

        return Response({'AVISO': payment_message, 'Confirmación de pago': final_message}, 
                        status=status.HTTP_200_OK)