import os
import django
from datetime import datetime

# Configurando el entorno Django para poder acceder a los modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

# Importa los modelos después de configurar Django
from apps.productos.models import Producto, Precio

def main():
    # Solicitar datos del usuario para crear un producto
    print("Ingrese los detalles del producto:")
    codigo_producto = input("Código del producto: ")
    codigo = input("Código secundario del producto: ")
    marca = input("Marca del producto: ")
    modelo = input("Modelo del producto: ")
    nombre = input("Nombre del producto: ")
    stock = int(input("Stock inicial del producto: "))

    # Crear el producto en la base de datos
    producto = Producto.objects.create(
        codigo_producto=codigo_producto,
        codigo=codigo,
        marca=marca,
        modelo=modelo,
        nombre=nombre,
        stock=stock
    )

    # Solicitar detalles para el precio del producto
    print("Ingrese el precio del producto ejemplo: 89090.99")
    valor = float(input("Precio del producto: "))
    
    # Crear el precio en la base de datos
    precio = Precio.objects.create(
        producto=producto,
        fecha=datetime.now(),
        valor=valor
    )
    
    print(f"Producto creado: {producto.nombre}")
    print(f"Precio asignado: ${precio.valor}")

if __name__ == "__main__":
    main()
