Enlace de repositorio github: https://github.com/OsvaLogic/E-commerce.git
1. Motor de Base de Datos Utilizado

Para este proyecto, estoy utilizando SQLite3 como motor de base de datos por defecto (o actualiza a PostgreSQL si configuras el settings.py), ideal para pruebas locales rápidas.

2. Descripción del Modelo de Datos

He definido mi estructura de datos en el archivo models.py utilizando las siguientes entidades y lógicas:

    Modelo Category: Lo utilizo para agrupar mis productos en categorías lógicas (como periféricos o hardware).

    Modelo Product: Es mi entidad principal. He incluido campos para el nombre, descripción, stock e imágenes. He aplicado una validación específica para asegurar que el precio siempre sea mayor a 0.

    Relación: He implementado una relación de muchos a uno (ForeignKey) para vincular cada producto con su categoría correspondiente.

3. Rutas Principales del Módulo de Administración

He habilitado las siguientes rutas para gestionar mi catálogo de productos:

    /products/: Aquí muestro el listado completo de mis productos.

    /products/create/: Utilizo esta ruta para desplegar el formulario de creación.

    /products/edit/<id>/: Aquí permito la edición de productos existentes.

    /products/delete/<id>/: Esta ruta la destino a la eliminación de registros.

Rutas de Cliente (Flujo de Compra):

    /: Página principal y catálogo público de productos.
    /login/ y /logout/: Autenticación de usuarios.
    /cart/: Visualización y gestión del carrito de compras (agregar, actualizar, eliminar).
    /checkout/: Confirmación de la compra y registro del pedido asociado al usuario.

4. Pasos para Ejecutar el Proyecto

Para que puedas desplegar mi proyecto localmente, sigue estos pasos que he preparado:

    Entorno virtual: Lo creo con python -m venv venv y lo activo según mi sistema operativo.

    Instalación: Ejecuto pip install -r requirements.txt para cargar las dependencias.

    Migraciones: Sincronizo mi base de datos con python manage.py makemigrations y python manage.py migrate.

    Ejecución: Inicio mi servidor de desarrollo con python manage.py runserver.

5. Credenciales de Prueba

Para probar el sistema, puedes utilizar los siguientes usuarios:
* **Administrador:** Usuario: `admin_test` | Contraseña: `password123` (Acceso total al CRUD de productos)
* **Cliente:** Usuario: `cliente_test` | Contraseña: `password123` (Acceso al catálogo y carrito de compras)

6. Evidencias del Proyecto

A continuación, presento las capturas de pantalla que demuestran el funcionamiento de los requerimientos:

**Listado de Productos:**
![Listado de Productos](<Capturas de pantalla/Captura de pantalla 2026-03-29 200955.png>)

**Formulario de Creación/Edición:**
![Formulario de Producto](<Capturas de pantalla/Captura de pantalla 2026-03-29 195510.png>)

**Panel de Administración de Django:**
![Panel Administrativo](<Capturas de pantalla/Captura de pantalla 2026-04-08 220912.png>)