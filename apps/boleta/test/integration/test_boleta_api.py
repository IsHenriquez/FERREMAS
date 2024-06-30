import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.addproductos.models import Cart, CartItem
from apps.productos.models import Producto, Precio
from apps.boleta.models import Boleta

@pytest.mark.django_db
class TestBoletaIntegrationAPI:
    def setup_method(self):
        self.client = APIClient()
        self.producto = Producto.objects.create(codigo_producto="PROD123", nombre="Producto de Prueba", stock=10)
        Precio.objects.create(producto=self.producto, fecha='2023-01-01', valor=100.00)
        self.cart = Cart.objects.create(estado='pendiente')
        CartItem.objects.create(cart=self.cart, product=self.producto, quantity=2)
        self.cart.update_total()

    def test_no_generar_y_no_obtener_boleta_carrito_no_pagado(self):
        """
        Verifica que no se puede generar una boleta para un carrito no pagado y que no se puede obtener una boleta inexistente.
        """
        url_generar = reverse('boleta:generar-boleta')
        data = {'cart_id': self.cart.id}

        response_generar = self.client.post(url_generar, data, format='json')
        assert response_generar.status_code == status.HTTP_400_BAD_REQUEST
        assert response_generar.data['error'] == 'No se puede generar la boleta porque el carrito no está pagado'

        url_obtener = reverse('boleta:obtener-boleta', kwargs={'cart_id': self.cart.id})
        response_obtener = self.client.get(url_obtener)
        assert response_obtener.status_code == status.HTTP_404_NOT_FOUND
        assert response_obtener.data['error'] == 'Boleta no encontrada'

    def test_intentar_generar_boleta_ya_existente(self):
        """
        Verifica que no se puede generar una boleta ya existente para un carrito pagado.
        """
        # Cambiar el estado del carrito a pagado y crear una boleta
        self.cart.estado = 'pagado'
        self.cart.save()

        Boleta.objects.create(
            numero_boleta=f'BOLETA-{self.cart.id}',
            productos=[{
                'codigo_producto': self.cart.items.first().product.codigo_producto,
                'nombre_producto': self.cart.items.first().product.nombre,
                'cantidad': 2,
                'precio_unitario': str(self.cart.items.first().product.precio.latest('fecha').valor),
                'subtotal': str(self.cart.items.first().product.precio.latest('fecha').valor * 2)
            }],
            precio_total=str(self.cart.precio_total),
            cantidad_productos=2
        )

        url = reverse('boleta:generar-boleta')
        data = {'cart_id': self.cart.id}

        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'La boleta para este carrito ya existe'

    def test_generar_y_obtener_boleta_carrito_pagado(self):
        """
        Verifica que se puede generar una boleta para un carrito pagado y luego obtenerla correctamente.
        """
        # Cambiar el estado del carrito a pagado
        self.cart.estado = 'pagado'
        self.cart.save()

        url_generar = reverse('boleta:generar-boleta')
        data = {'cart_id': self.cart.id}

        response_generar = self.client.post(url_generar, data, format='json')
        assert response_generar.status_code == status.HTTP_201_CREATED
        assert response_generar.data['numero_boleta'] == f'BOLETA-{self.cart.id}'
        assert str(response_generar.data['precio_total']) == str(self.cart.precio_total)
        assert response_generar.data['cantidad_productos'] == 2

        url_obtener = reverse('boleta:obtener-boleta', kwargs={'cart_id': self.cart.id})
        response_obtener = self.client.get(url_obtener)
        assert response_obtener.status_code == status.HTTP_200_OK
        assert response_obtener.data['numero_boleta'] == f'BOLETA-{self.cart.id}'
        assert str(response_obtener.data['precio_total']) == str(self.cart.precio_total)
        assert response_obtener.data['cantidad_productos'] == 2

    def test_obtener_boleta_existente_despues_de_intento_fallido(self):
        """
        Verifica que se puede obtener una boleta existente después de un intento fallido de generación para un carrito no pagado, seguido por un cambio de estado a pagado y generación exitosa.
        """
        url_generar = reverse('boleta:generar-boleta')
        data = {'cart_id': self.cart.id}

        response_generar_fallido = self.client.post(url_generar, data, format='json')
        assert response_generar_fallido.status_code == status.HTTP_400_BAD_REQUEST
        assert response_generar_fallido.data['error'] == 'No se puede generar la boleta porque el carrito no está pagado'

        # Cambiar el estado del carrito a pagado
        self.cart.estado = 'pagado'
        self.cart.save()

        response_generar_exitoso = self.client.post(url_generar, data, format='json')
        assert response_generar_exitoso.status_code == status.HTTP_201_CREATED
        assert response_generar_exitoso.data['numero_boleta'] == f'BOLETA-{self.cart.id}'
        assert str(response_generar_exitoso.data['precio_total']) == str(self.cart.precio_total)
        assert response_generar_exitoso.data['cantidad_productos'] == 2

        url_obtener = reverse('boleta:obtener-boleta', kwargs={'cart_id': self.cart.id})
        response_obtener = self.client.get(url_obtener)
        assert response_obtener.status_code == status.HTTP_200_OK
        assert response_obtener.data['numero_boleta'] == f'BOLETA-{self.cart.id}'
        assert str(response_obtener.data['precio_total']) == str(self.cart.precio_total)
        assert response_obtener.data['cantidad_productos'] == 2
