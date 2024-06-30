# Create your models here.
from django.db import models
from django.conf import settings
from apps.addproductos.models import Cart  # Asumiendo que `Cart` está definido en `addproductos`

class HistorialCompra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historial_compras')
    carrito = models.OneToOneField(Cart, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Historial de compra de {self.usuario.username} - {self.fecha_compra}'
