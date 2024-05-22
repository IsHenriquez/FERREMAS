from django.db import models
from addproductos.models import Cart

class Pedido(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.id}"
