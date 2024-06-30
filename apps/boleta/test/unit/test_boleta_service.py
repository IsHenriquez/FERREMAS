import pytest
from rest_framework.test import APIClient
from rest_framework import status
from apps.addproductos.models import Cart

@pytest.mark.django_db
class TestBoletaAPI:
    def test_generar_boleta_cart_id_requerido(self):
        """
        Prueba para verificar que el cart_id es requerido al generar una boleta.
        """
        client = APIClient()
        url = '/api/boleta/generar/'
        data = {}
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Cart ID es requerido'

    def test_generar_boleta_carrito_no_existe(self):
        """
        Prueba para verificar que no se puede generar una boleta si el carrito no existe.
        """
        client = APIClient()
        url = '/api/boleta/generar/'
        data = {'cart_id': 999}
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'El carrito no existe'

    def test_generar_boleta_cart_id_debe_ser_positivo(self):
        """
        Prueba para verificar que el cart_id debe ser un número positivo.
        """
        client = APIClient()
        url = '/api/boleta/generar/'
        data = {'cart_id': -1} 
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Cart ID debe ser un número positivo'

    def test_obtener_boleta_boleta_no_encontrada(self):
        """
        Prueba para verificar que se maneja correctamente cuando la boleta no existe.
        """
        client = APIClient()
        url = '/api/boleta/999/'  
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'Boleta no encontrada'
