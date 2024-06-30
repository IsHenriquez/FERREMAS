from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Boleta
from apps.addproductos.models import Cart
from django.utils import timezone
from decimal import Decimal

@api_view(['POST'])
def generar_boleta(request):
    cart_id = request.data.get('cart_id')
    if not cart_id:
        return Response({'error': 'Cart ID es requerido'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validación para asegurarse de que el cart_id es un número positivo
    if not isinstance(cart_id, int) or cart_id <= 0:
        return Response({'error': 'Cart ID debe ser un número positivo'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({'error': 'El carrito no existe'}, status=status.HTTP_404_NOT_FOUND)

    if cart.estado != 'pagado':
        return Response({'error': 'No se puede generar la boleta porque el carrito no está pagado'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si ya existe una boleta para este carrito
    if Boleta.objects.filter(numero_boleta=f'BOLETA-{cart_id}').exists():
        return Response({'error': 'La boleta para este carrito ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    productos = []
    cantidad_total = 0

    for item in cart.items.all():
        productos.append({
            'codigo_producto': item.product.codigo_producto,
            'nombre_producto': item.product.nombre,
            'cantidad': item.quantity,
            'precio_unitario': str(item.product.precio.latest('fecha').valor),  # Convertir a string
            'subtotal': str(item.product.precio.latest('fecha').valor * item.quantity)  # Calcular subtotal y convertir a string
        })
        cantidad_total += item.quantity

    try:
        boleta = Boleta.objects.create(
            numero_boleta=f'BOLETA-{cart_id}',
            productos=productos,
            precio_total=str(cart.precio_total),  # Convertir a string
            fecha_emision=timezone.now(),
            cantidad_productos=cantidad_total
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'numero_boleta': boleta.numero_boleta,
        'productos': boleta.productos,
        'precio_total': boleta.precio_total,
        'fecha_emision': boleta.fecha_emision,
        'cantidad_productos': boleta.cantidad_productos
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def obtener_boleta(request, cart_id):
    if not isinstance(cart_id, int) or cart_id <= 0:
        return Response({'error': 'Cart ID debe ser un número positivo'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        boleta = Boleta.objects.get(numero_boleta=f'BOLETA-{cart_id}')
    except Boleta.DoesNotExist:
        return Response({'error': 'Boleta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'numero_boleta': boleta.numero_boleta,
        'productos': boleta.productos,
        'precio_total': boleta.precio_total,
        'fecha_emision': boleta.fecha_emision,
        'cantidad_productos': boleta.cantidad_productos
    }, status=status.HTTP_200_OK)
