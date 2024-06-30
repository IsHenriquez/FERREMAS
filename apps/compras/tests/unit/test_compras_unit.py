'''
Pruebas unitarias para app compras
'''

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.addproductos.models import Cart, CartItem
from apps.productos.models import Precio, Producto

@pytest.mark.django_db
def test_finalizar_compra():
    producto = Producto.objects.create(
        codigo_producto="12345",
        nombre="TestProducto",
        stock=10
    )
    Precio.objects.create(producto=producto, fecha='2023-01-01', valor=100.00)
    cart = Cart.objects.create(precio_total=100)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=1)

    client = APIClient()
    url = reverse('finalizar_compra')

    data = {'cart_id': cart.id}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['Confirmación de pago'] == "Compra realizada!"
    assert Cart.objects.filter(id=cart.id).exists()  # Verificar que el carrito sigue existiendo
    assert Cart.objects.get(id=cart.id).estado == 'pagado'  # Verificar que el estado del carrito es 'pagado'

@pytest.mark.django_db
def test_finalizar_compra_stock_insuficiente():
    # Configurar datos de prueba
    producto = Producto.objects.create(
        codigo_producto="12345",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="12345",
        nombre="TestProducto",
        stock=1
    )
    cart = Cart.objects.create(precio_total=100)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=2)

    client = APIClient()
    url = reverse('finalizar_compra')

    # Simular solicitud POST
    data = {'cart_id': cart.id}
    response = client.post(url, data, format='json')

    # Verificar que se recibe un error 400 y el mensaje adecuado
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Stock insuficiente para el producto' in response.data['error']

@pytest.mark.django_db
def test_actualizar_stock_despues_de_compra():
    # Configurar datos de prueba
    producto = Producto.objects.create(
        codigo_producto="12345",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="12345",
        nombre="TestProducto",
        stock=10
    )
    cart = Cart.objects.create(precio_total=100)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=2)

    client = APIClient()
    url = reverse('finalizar_compra')

    data = {'cart_id': cart.id}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['Confirmación de pago'] == "Compra realizada!"

    producto_actualizado = Producto.objects.get(id=producto.id)
    assert producto_actualizado.stock == 8

@pytest.mark.django_db
def test_finalizar_compra_carrito_no_existente():
    producto = Producto.objects.create(
        codigo_producto="12345",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="12345",
        nombre="TestProducto",
        stock=10
    )
    cart = Cart.objects.create(precio_total=100)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=1)

    client = APIClient()
    url = reverse('finalizar_compra')

    data = {'cart_id': 999}  # ID de carrito que no existe
    response = client.post(url, data, format='json')

    # Verificar el estado de respuesta y mensaje de error
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == "El carrito no existe"

@pytest.mark.django_db
def test_stock_insuficiente_finalizar_compra():
    # Configurar datos de prueba
    producto = Producto.objects.create(
        codigo_producto="67890",
        marca="TestMarca",
        modelo="TestModelo",
        codigo="67890",
        nombre="ProductoSinStock",
        stock=0  # Producto sin stock
    )
    cart = Cart.objects.create(precio_total=50)  # Precio total no debería importar para esta prueba
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=1)

    client = APIClient()
    url = reverse('finalizar_compra')

    # Simular solicitud POST
    data = {'cart_id': cart.id}
    response = client.post(url, data, format='json')

    # Verificar el estado de la respuesta y los datos devueltos
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Stock insuficiente para el producto ProductoSinStock' in response.data['error']
    assert Cart.objects.filter(id=cart.id).exists() is True  # El carrito no debería eliminarse

@pytest.mark.django_db
def test_guardar_carrito_al_finalizar_compra():
    producto = Producto.objects.create(
        codigo_producto="11111",
        nombre="ProductoTest",
        stock=5
    )
    Precio.objects.create(producto=producto, fecha='2023-01-01', valor=50.00)
    cart = Cart.objects.create(precio_total=50)
    cart_item = CartItem.objects.create(cart=cart, product=producto, quantity=2)

    client = APIClient()
    url = reverse('finalizar_compra')

    data = {'cart_id': cart.id}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Cart.objects.filter(id=cart.id).exists()  # Verificar que el carrito sigue existiendo
    assert Cart.objects.get(id=cart.id).estado == 'pagado'  # Verificar que el estado del carrito es 'pagado'

    # Verificar que el stock del producto se haya actualizado
    producto_actualizado = Producto.objects.get(id=producto.id)
    assert producto_actualizado.stock == 3  # El stock original era 5 y se compraron 2 unidades

    # Verificar el mensaje de confirmación de pago
    assert response.data['Confirmación de pago'] == "Compra realizada!"