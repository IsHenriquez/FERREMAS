
# FERREMAS

> [!NOTE]
> **Puedes revisar la documentación en https://documenter.getpostman.com/view/34610614/2sA3Qqgsaz** 

También se encuentra una copia de la documentación en API_FERREMAS_DOCUMENTACION, dentro de la carpeta del proyecto


# Autores

- [@Isadora Henríquez](https://github.com/IsHenriquez)
- [@Adolfo maza](https://github.com/aamzp)
- [@Benjamín Araya](https://github.com/benja2203)


# Instalación y configuración

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
pip install -r requirement.txt
```

### 4. Ejecutar el servidor
```bash
python manage.py runserver
```

# Instrucciones de prueba

**NOTA: Se recomienda emplear Postman para los siguientes pasos**

### Ingrese datos de prueba

```bash
# Ejecute Agregarproducto.py
python Agregarproducto.py
# Siga las instrucciones de la terminal para generar datos de prueba
```

### 1. Endpoint API1 (Método HTTP GET)


```bash
# Para consultar todos los productos ingrese la siguiente URL y presione send:
http://127.0.0.1:8000/api/productos/

# Para consultar productos especificos ingrese la siguiente URL y al final colocar el codigo del producto por ejemplo:
http://127.0.0.1:8000/api/productos/FER-54321
```

### 2. Endpoint API2 (Método HTTP POST)
* En Postman, dentro de la sección body, ingrese los datos en raw para generar carrito de compras. Puede usar los creados por usted en el paso optativo, o los contenidos en la base de datos. Siga este ejemplo para ingresar datos.
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

### 3. Endpoint API3 (Método HTTP POST)
* En Postman, dentro de la sección body, ingrese los datos requeridos ("cart_id") en body con raw.
```bash
# Recuerde el número del carrito anterior.
{
    "cart_id": SU NÚMERO DE CARRITO
}
```
* Ingrese la siguiente URL: http://127.0.0.1:8000/api/finalizar_compra/ y apriete Send.

