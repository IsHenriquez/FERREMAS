import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestAccountAPI:
    def test_user_registration_successfully(self):
        """
        Test para verificar que el endpoint de registro de usuario funciona correctamente.
        """
        client = APIClient()

        url = 'http://127.0.0.1:8000/api/carrito/'

        data = {
            'codigo_producto': 'testuser',
            'quantity': 'dfdfsf' 
        }

        response = client.post(url, data, format='json')
        
        print(response)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert 'error' in response.data

        assert 'La lista de productos está vacía' in response.data['error']