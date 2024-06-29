from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.productos.models import Producto, Precio
from apps.addproductos.models import Cart, CartItem
from rest_framework import status

@api_view(['POST'])
def add_to_cart(request):
    # Extraer la lista de productos del cuerpo de la solicitud
    products = request.data.get('products', [])
    if not products:
        # Si no hay productos, devolver un error
        return Response({'error': 'La lista de productos está vacía'}, status=status.HTTP_400_BAD_REQUEST)

    # Crear un nuevo carrito y preparar estructuras para manejo de datos y errores
    cart = Cart.objects.create()
    response_data = []
    errors = []

    # Iterar sobre cada producto solicitado
    for product_data in products:
        codigo_producto = product_data.get('codigo_producto')
        quantity = product_data.get('quantity', 1)

        # Validaciones de entrada básicas
        if not codigo_producto:
            errors.append({'codigo_producto': None, 'error': 'Falta campo codigo_producto o está vacío', 'status': 'failed'})
            continue

        if not isinstance(codigo_producto, str):
            errors.append({'codigo_producto': codigo_producto, 'error': 'El código de producto debe ser texto', 'status': 'failed'})
            continue

        if not isinstance(quantity, int) or quantity < 1:
            errors.append({'codigo_producto': codigo_producto, 'error': 'Ingrese cantidad con número positivo', 'status': 'failed'})
            continue

        try:
            # Obtener el producto por el código
            producto = Producto.objects.get(codigo_producto=codigo_producto)

            # Comprobar si hay suficiente stock
            if producto.stock < quantity:
                errors.append({'codigo_producto': codigo_producto, 'error': 'Stock insuficiente', 'status': 'failed'})
                continue

            # Obtener el precio más reciente del producto
            latest_price = Precio.objects.filter(producto=producto).latest('fecha').valor

            # Crear un nuevo ítem en el carrito
            CartItem.objects.create(
                cart=cart,
                product=producto,
                quantity=quantity
            )

            # Añadir datos del producto añadido a la respuesta
            response_data.append({
                'codigo_producto': codigo_producto,
                'nombre_producto': producto.nombre,
                'precio_unitario': latest_price,
                'cantidad': quantity,
                'precio_total_item': latest_price * quantity,
                'status': 'Producto agregado correctamente'
            })

        except Producto.DoesNotExist:
            errors.append({'codigo_producto': codigo_producto, 'error': 'Producto no encontrado', 'status': 'failed'})
        except Precio.DoesNotExist:
            errors.append({'codigo_producto': codigo_producto, 'error': 'No hay un precio disponible para el producto', 'status': 'failed'})

    # Finalizar la respuesta basada en si hubo errores o no
    if not errors:
        # Si no hay errores, actualizar el total del carrito y devolver la respuesta de éxito
        cart.update_total()
        return Response({'cart_id': 'Su numero de carrito a pagar es --> ' + str(cart.id), 'products': response_data, 'precio_total': cart.precio_total}, status=status.HTTP_201_CREATED)
    else:
        # Si hay errores, eliminar el carrito creado y devolver los errores
        cart.delete()
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
