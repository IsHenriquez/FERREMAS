
# FERREMAS

> [!NOTE]
> **Puedes revisar la documentación en https://documenter.getpostman.com/view/34610614/2sA3Qqgsaz** 

También se encuentra una copia de la documentación en API_FERREMAS_DOCUMENTACION, dentro de la carpeta del proyecto


# Autores

- [@Isadora Henríquez](https://github.com/IsHenriquez)
- [@Adolfo maza](https://github.com/aamzp)
- [@Benjamín Araya](https://github.com/benja2203)


# Instalación y configuración

> [!IMPORTANT]
> **Debe tener instalado python y pip antes de seguir con la instalación y configuración** 

### 1. Clonar repositorio
```bash
git clone https://github.com/IsHenriquez/FERREMAS.git
```



### 2. Instalación y configuracion de `virtualenv` 
```bash 
# Instalamos virtualenv en caso de no tenerlo
pip3 install virtualenv
```
```bash
# Creamos el entorno
python -m venv myenv
```
```bash
#Activamos el entorno
myenv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor
```bash
python manage.py runserver
```

## Ejecutar Tests

- Para correr los test ingrese el siguiendo comando en la terminal

```bash
  pytest
```

# Instrucciones de prueba

**NOTA: Se recomienda emplear Postman para los siguientes pasos**

### Ingrese datos de prueba

```bash
# Ejecute Agregarproducto.py
python Agregarproducto.py
# Siga las instrucciones de la terminal para generar datos de prueba
```

### 1. Endpoint productos (Método HTTP GET)
- Puede usar los creados por usted en el paso de "Ingresar datos de prueba", o los contenidos en la base de datos. Siga el ejemplo de recuadro de abajo

```bash
# Para consultar todos los productos ingrese la siguiente URL y presione send:
http://127.0.0.1:8000/api/productos/

# Para consultar productos especificos ingrese la siguiente URL y al final colocar el codigo del producto por ejemplo:
http://127.0.0.1:8000/api/productos/FER-54321
```

### 2. Endpoint Crear producto (Método HTTP POST)

* Para crear productos, ingrese a la url: http://127.0.0.1:8000/api/productos/admin/create/
* Dentro de las secciónes ingresar a body, seleccione raw y cambiar formato "Text" a formato "Json".
* Siga el ejemplo del recuadro Body que esta mas abajo para ingresar datos.
* El código de producto a crear, no debe existir
* Apriete send para crear el producto ingresado

```bash
# Datos de ejemplo
{
    
    "codigo_producto": "PROD1234",
        "marca": "Marca1",
        "modelo": "Modelo1",
        "codigo": "COD001",
        "nombre": "Producto 1",
        "stock": 10
}
```

### 3. Endpoint Actualizar producto (Método HTTP PATCH)
* Para actualizar un producto, primero debe identificar el codigo_producto del producto a editar
* Luego, ingrese a la url: http://127.0.0.1:8000/api/productos/{codigo_producto}/admin/edit/ , reemplazando la variable {codigo_producto} con el codigo correspondiente
* Dentro de las secciónes ingresar a body, seleccione raw y cambiar formato "Text" a formato "Json".
* Siga el ejemplo del recuadro Body que esta mas abajo para ingresar datos.
* Apriete send para editar el producto en cuestión


```bash
# Datos de ejemplo
{
    
    "marca": "ModeloABC"

}
```

### 4. Endpoint Eliminar producto (Método HTTP DELETE)

* Para eliminar un producto, primero debe identificar el codigo_producto del producto a eliminar
* Luego, ingrese a la url: http://127.0.0.1:8000/api/productos/{codigo_producto}/admin/delete/ , reemplazando la variable {codigo_producto} con el codigo correspondiente
* Apriete send para eliminar el producto en cuestión


### 5. Endpoint Agregar producto al carrito (Método HTTP POST)
- Dentro de las secciónes ingresar a body, seleccione raw y cambiar formato "Text" a formato "Json".
- Para generar carrito de compras. Puede usar los creados por usted en el paso de "Ingresar datos de prueba", o los contenidos en la base de datos. Siga el ejemplo del recuadro Body que esta mas abajo para ingresar datos.

```bash
# Datos de ejemplo
{
  "products": [
    {"codigo_producto": "FER-543210", "quantity": 3}
    {"codigo_producto": "FER-12345", "quantity": 1}
  ]
}
```
* Ingrese la siguiente URL: http://127.0.0.1:8000/api/carrito/ y apriete Send.
* La respuesta de la API le entregará una id de carrito, esto es importante para el funcionamiento de API3.

### 6. Endpoint Pagar carrito (Método HTTP POST)
- Dentro de las secciónes ingresar a body, seleccione raw y cambiar formato "Text" a formato "Json".
- Siga el ejemplo del recuadro Body que esta mas abajo para ingresar datos.
- Con el numero que le dio en la respuesta de la api de agregar producto "cart_id" ingresarlo en el body como se muestra

```bash
# Recuerde el número del carrito anterior.
{
    "cart_id": SU NÚMERO DE CARRITO
}
```
* Ingrese la siguiente URL: http://127.0.0.1:8000/api/finalizar_compra/ y apriete Send.



### 7. Endpoint para generar boleta (Método HTTP POST)

- Dentro de las secciones ingresar a body, seleccione raw y cambiar formato "Text" a formato "Json".
- Con el número del carrito pagado, ingréselo en la URL como se muestra y apriete send:

```bash
# Recuerde el número del carrito anterior.
{
    "cart_id": SU NÚMERO DE CARRITO
}
```

### 8. Endpoint para obtener boleta (Método HTTP GET)

- Para obtener los detalles de la boleta, use el cart_id del carrito pagado en la URL y apriete send:

```bash
http://127.0.0.1:8000/api/boleta/Numero_carrito/
```
