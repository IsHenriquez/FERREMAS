from django.db import models
from apps.productos.models import Producto  # Importa el modelo Producto desde la aplicación productos

# Create your models here.

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def update_total(self):
        self.precio_total = sum(item.product.precio.latest('fecha').valor * item.quantity for item in self.items.all())
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

