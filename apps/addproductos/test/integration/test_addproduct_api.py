import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from apps.productos.models import Producto, Precio

@pytest.mark.django_db
class TestAddToCartIntegration:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('addproductos:carrito')  # Asegúrate de que esta URL es correcta en tu configuración de urls.py
        self.product1 = Producto.objects.create(codigo_producto="PROD-123", nombre="Producto Uno", stock=10)
        self.product2 = Producto.objects.create(codigo_producto="PROD-456", nombre="Producto Dos", stock=5)
        self.product3 = Producto.objects.create(codigo_producto="PROD-543", nombre="Producto Tres", stock=0)
        Precio.objects.create(producto=self.product1, fecha='2023-01-01', valor=100.00)
        Precio.objects.create(producto=self.product2, fecha='2023-01-01', valor=200.00)
        Precio.objects.create(producto=self.product3, fecha='2023-01-01', valor=300.00)

    def test_add_multiple_products_to_cart(self):
        """
        Test para verificar que se pueden agregar dos productos diferentes al carrito.
        """
        data = {
            'products': [
                {'codigo_producto': self.product1.codigo_producto, 'quantity': 2},
                {'codigo_producto': self.product2.codigo_producto, 'quantity': 3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data['products']) == 2
        assert response.data['products'][0]['codigo_producto'] == self.product1.codigo_producto
        assert response.data['products'][1]['codigo_producto'] == self.product2.codigo_producto


    def test_add_out_of_stock_product(self):
        """
        Test para verificar que la API maneja correctamente un producto que está fuera de stock.
        """
        data = {
            'products': [
                {'codigo_producto': self.product3.codigo_producto, 'quantity': 1}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['error'] == 'No queda stock de este producto'


    def test_add_product_with_invalid_quantity(self):
        """
        Test para verificar que la API rechaza correctamente cantidades inválidas (cero o negativas).
        """
        data = {
            'products': [
                {'codigo_producto': self.product1.codigo_producto, 'quantity': -1}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert all('Ingrese cantidad con número positivo' in error['error'] for error in response.data['errors'])


    def test_add_product_missing_codigo(self):
        """
        Test para verificar que se maneja correctamente cuando falta el atributo codigo_producto.
        """
        data = {
            'products': [
                {'quantity': 2}  # Falta el campo codigo_producto
            ]
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'errors' in response.data
        assert response.data['errors'][0]['error'] == 'Falta campo codigo_producto o está vacío'