import pytest
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from apps.productos.models import Producto, Precio
from apps.productos.serializers import ProductoSerializer





@pytest.mark.django_db
class TestIntegrationProducts(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.producto_data_prueba = {
            'codigo_producto': 'PROD001',
            'marca': 'Marca1',
            'modelo': 'Modelo1',
            'codigo': 'COD001',
            'nombre': 'Producto 1',
            'stock': 10
        }

        self.producto_nuevo_modelo = {
            "marca": "ModeloABC"
        }

        self.producto_nuevo_codigo = {
            "codigo_producto": "ddd222"
        }


    def test_create_and_view_product(self):

#crear un producto y luego ver la lista, si es que se ve

        client = APIClient()
        producto_data = self.producto_data_prueba

        response_create = client.post('/api/productos/admin/create/', producto_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        

        response_get = client.get('/api/productos/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        
        productos = response_get.json()
        ultimo_item = productos[-1]        

        self.assertEqual(ultimo_item['codigo_producto'], producto_data['codigo_producto'])



 

    def test_edit_and_detailed_view(self):

#editar un producto y ver la lista, si es que se ve actualizado

        response_create = self.client.post('/api/productos/admin/create/', self.producto_data_prueba, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        
        new_code = response_create.data.get('codigo_producto')

        response_update = self.client.patch(f'/api/productos/{new_code}/admin/edit/', self.producto_nuevo_modelo, format='json')
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)


        response_get = self.client.get(f'/api/productos/{new_code}/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        self.assertEqual(self.producto_nuevo_modelo['marca'], response_get.data.get('marca'))



    def test_delete_and_notview_list(self):

#eliminar un producto y luego ver la lista, si es que no se ve

        response_create = self.client.post('/api/productos/admin/create/', self.producto_data_prueba, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        
        new_code = response_create.data.get('codigo_producto')

        response_delete = self.client.delete(f'/api/productos/{new_code}/admin/delete/')
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        response_get = self.client.get(f'/api/productos/')
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        productos = response_get.json()
        self.assertEqual(len(productos), 0)


    def test_editcode_and_failed_detailed_view(self):

#editar el codigo de un producto y luego intentar verlo unitariamente con el code antiguo, si es que no lo ve

        response_create = self.client.post('/api/productos/admin/create/', self.producto_data_prueba, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        
        new_code = response_create.data.get('codigo_producto')

        response_update = self.client.patch(f'/api/productos/{new_code}/admin/edit/', self.producto_nuevo_codigo, format='json')
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)


        response_get = self.client.get(f'/api/productos/{new_code}/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No Producto matches the given query', str(response_get.data))


            
        
        



'''
1 crear un producto y luego ver la lista, si es que se ve
2 editar un producto y ver la lista, si es que se ve actualizado
3 eliminar un producto y luego ver la lista, si es que no se ve
4 editar el codigo de un producto y luego intentar verlo unitariamente con el codigo antiguo, si es que no lo ve
'''