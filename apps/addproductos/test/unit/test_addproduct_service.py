import pytest
from rest_framework.test import APIClient
from rest_framework import status
from apps.productos.models import Producto, Precio

@pytest.mark.django_db
class TestAddProductToCartUnit:

    #Esta prueba asegura que la API rechaza un código de producto si este no es un string
    def test_invalid_product_code_format(self):
        client = APIClient()
        product = Producto.objects.create(codigo_producto="PROD123", nombre="Producto de Prueba", stock=10)
        Precio.objects.create(producto=product, fecha='2023-01-01', valor=100.00)
        data = {'products': [{'codigo_producto': 12345, 'quantity': 1}]}  # código de producto no es un string
        response = client.post('/api/carrito/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'El código de producto debe ser texto' in str(response.data)

#Esta prueba verifica que se pueda agregar un producto al carrito correctamente
    def test_add_product_to_cart_successfully(self):
        client = APIClient()
        product = Producto.objects.create(codigo_producto="PROD123", nombre="Producto de Prueba", stock=10)
        Precio.objects.create(producto=product, fecha='2023-01-01', valor=100.00)
        data = {'products': [{'codigo_producto': "PROD123", 'quantity': 1}]}
        response = client.post('/api/carrito/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'Producto agregado correctamente' in response.data['products'][0]['status']

#Esta prueba verifica que no se pueda agregar un producto que no exista
    def test_add_product_not_found(self):
        client = APIClient()
        data = {'products': [{'codigo_producto': "NONEXIST123", 'quantity': 1}]}
        response = client.post('/api/carrito/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Producto no encontrado' in response.data['errors'][0]['error']

#Esta prueba verifica que no se pueda agregar una cantidad de producto de exceda la cantidad actual
    def test_add_product_exceeding_stock(self):
        client = APIClient()
        product = Producto.objects.create(codigo_producto="PROD123", nombre="Producto de Prueba", stock=1)
        Precio.objects.create(producto=product, fecha='2023-01-01', valor=100.00)
        data = {'products': [{'codigo_producto': "PROD123", 'quantity': 2}]}
        response = client.post('/api/carrito/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        expected_error_message = f'Stock insuficiente. Solo quedan {product.stock} unidades'
        assert expected_error_message in response.data['errors'][0]['error']
