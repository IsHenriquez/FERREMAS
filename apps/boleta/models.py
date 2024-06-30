from django.db import models

class Boleta(models.Model):
    numero_boleta = models.CharField(max_length=20, unique=True)
    productos = models.JSONField()  # Puedes usar JSONField para almacenar una lista de productos
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    cantidad_productos = models.PositiveIntegerField()

    def __str__(self):
        return self.numero_boleta
