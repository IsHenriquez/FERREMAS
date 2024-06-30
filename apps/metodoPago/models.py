# Create your models here.
from django.db import models
from django.conf import settings

class MetodoPago(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metodos_pago')
    tipo = models.CharField(max_length=50)  # e.g., 'Tarjeta de Crédito', 'PayPal', etc.
    proveedor = models.CharField(max_length=50)  # e.g., 'Visa', 'MasterCard', etc.
    numero_tarjeta = models.CharField(max_length=20)
    fecha_expiracion = models.CharField(max_length=5)  # MM/AA
    cvv = models.CharField(max_length=4)
    nombre_titular = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tipo} - {self.proveedor} - {self.numero_tarjeta}'
