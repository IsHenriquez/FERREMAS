from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
import time 

@api_view(['POST'])
def finalizar_compra(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({'error': 'El carrito no existe'}, status=status.HTTP_404_NOT_FOUND)

    # Simulación de proceso de pago
    payment_message = "Trasladando a portal de pago con tarjeta de crédito..."
    print(payment_message)
    time.sleep(5)
    # Finalizar la compra eliminando el carrito
    cart.delete()

    # Mensaje final de compra realizada
    time.sleep(5)
    final_message = "Compra realizada!"

    return Response({'AVISO': payment_message, 'Confirmación de pago': final_message}, 
                    status=status.HTTP_200_OK)