from django.db import models

# Create your models here.

class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje de descuento
    fecha_expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.codigo} - {self.descuento}%'
