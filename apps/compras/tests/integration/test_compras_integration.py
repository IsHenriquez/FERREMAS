'''
Pruebas de integración para app compras
'''
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.compras.models import Pedido
from apps.addproductos.models import Cart, CartItem
from apps.productos.models import Producto

@pytest.mark.django_db
def test_integracion_finalizar_compra():
    # Configurar datos de prueba
    producto = Producto.objects.create(
        codigo_producto="22222",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="22222",
        nombre="ProductoPrueba",
        stock=5
    )
    cart = Cart.objects.create(precio_total=75)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=3)

    client = APIClient()
    url_finalizar_compra = reverse('finalizar_compra')

    # Simular solicitud POST para finalizar la compra
    data = {'cart_id': cart.id}
    response_finalizar = client.post(url_finalizar_compra, data, format='json')

    # Verificar el estado de la respuesta y los datos devueltos en finalizar compra
    assert response_finalizar.status_code == status.HTTP_200_OK
    assert response_finalizar.data['Confirmación de pago'] == "Compra realizada!"
    assert Cart.objects.filter(id=cart.id).exists() is False  # Verificar que el carrito se haya eliminado

    # Verificar que el stock del producto se haya actualizado
    producto_actualizado = Producto.objects.get(id=producto.id)
    assert producto_actualizado.stock == 2  # El stock original era 5 y se compraron 3 unidades

@pytest.mark.django_db
def test_integracion_finalizar_compra_stock_insuficiente():
    # Configurar datos de prueba
    producto = Producto.objects.create(
        codigo_producto="33333",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="33333",
        nombre="ProductoInsuficiente",
        stock=2  # Stock insuficiente
    )
    cart = Cart.objects.create(precio_total=50)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=3)

    client = APIClient()
    url_finalizar_compra = reverse('finalizar_compra')

    # Simular solicitud POST para finalizar la compra
    data = {'cart_id': cart.id}
    response_finalizar = client.post(url_finalizar_compra, data, format='json')

    # Verificar el estado de la respuesta y los datos devueltos en finalizar compra
    assert response_finalizar.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Stock insuficiente para el producto' in response_finalizar.data['error']

    # Verificar que el carrito no se haya eliminado
    assert Cart.objects.filter(id=cart.id).exists()

    # Verificar que el stock del producto no se haya actualizado
    producto_actualizado = Producto.objects.get(id=producto.id)
    assert producto_actualizado.stock == 2  # El stock original era 2 y se intentaron comprar 3 unidades

@pytest.mark.django_db
def test_integracion_finalizar_compra_carrito_no_existente():
    client = APIClient()
    url_finalizar_compra = reverse('finalizar_compra')

    # Simular solicitud POST para finalizar la compra con un carrito inexistente
    data = {'cart_id': 999}  # ID de carrito que no existe
    response_finalizar = client.post(url_finalizar_compra, data, format='json')

    # Verificar el estado de la respuesta y los datos devueltos en finalizar compra
    assert response_finalizar.status_code == status.HTTP_404_NOT_FOUND
    assert 'El carrito no existe' in response_finalizar.data['error']

@pytest.mark.django_db
def test_integracion_finalizar_compra_eliminacion_carrito():
    # Configurar datos de prueba
    producto = Producto.objects.create(
        codigo_producto="44444",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="44444",
        nombre="ProductoFinalizarCompra",
        stock=10
    )
    cart = Cart.objects.create(precio_total=100)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=2)

    client = APIClient()
    url_finalizar_compra = reverse('finalizar_compra')

    # Simular solicitud POST para finalizar la compra
    data = {'cart_id': cart.id}
    response_finalizar = client.post(url_finalizar_compra, data, format='json')

    # Verificar el estado de la respuesta y los datos devueltos en finalizar compra
    assert response_finalizar.status_code == status.HTTP_200_OK
    assert response_finalizar.data['Confirmación de pago'] == "Compra realizada!"

    # Verificar que el carrito se haya eliminado
    assert not Cart.objects.filter(id=cart.id).exists()

    # Verificar que el stock del producto se haya actualizado
    producto_actualizado = Producto.objects.get(id=producto.id)
    assert producto_actualizado.stock == 8  # El stock original era 10 y se compraron 2 unidades