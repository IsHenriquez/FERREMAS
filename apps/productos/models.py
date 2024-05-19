from django.db import models

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=10, unique=True, blank=False)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    nombre = models.TextField(max_length=100)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

class Precio(models.Model):
    producto = models.ForeignKey(Producto, related_name='precio', on_delete=models.CASCADE)
    fecha = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha}: ${self.valor}"

