import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.productos.models import Producto, Precio
from apps.productos.serializers import ProductoSerializer


producto_data_prueba = {
    "codigo_producto": "PROD001",
        "marca": "Marca1",
        "modelo": "Modelo1",
        "codigo": "COD001",
        "nombre": "Producto 1",
        "stock": 10
}

id_no_existente = 1


@pytest.mark.django_db
class TestUnitProducts:

    def test_product_without_price(self):

#se puede agregar un producto sin precio

        client = APIClient()
        producto = producto_data_prueba
        response = client.post('/api/productos/admin/create/', producto, format='json')
        assert response.status_code == status.HTTP_201_CREATED


    def test_wrong_delete_nonexistent_code(self):

#al eliminar un producto, si pongo un codigo de producto que no existe, me indica que ningun producto coincide

        client = APIClient()
        response = client.delete(f'/api/productos/{id_no_existente}/admin/delete/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'No Producto matches the given query' in str(response.data)


    def test_nonexistent_code_detail(self):

#al ver el get detalle de producto, si pongo un codigo de producto que no existe, me indica que ningun producto coincide

        client = APIClient()
        response = client.get(f'/api/productos/{id_no_existente}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'No Producto matches the given query' in str(response.data)


    def test_wrong_update_nonexistent_code(self):

#al updatear un producto, si pongo un codigo de producto que no existe, me indica que ningun producto coincide

        client = APIClient()


        producto = producto_data_prueba
        response = client.patch(f'/api/productos/{id_no_existente}/admin/edit/', producto, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'No Producto matches the given query' in str(response.data)


