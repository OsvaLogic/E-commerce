# Osva.Logic - E-Commerce Gamer (Módulo 7 - Acceso a Datos)

## 1. Propósito del Proyecto
Implementación de la capa de acceso a datos de un e-commerce utilizando Django y su ORM. Este módulo permite administrar un catálogo de productos mediante operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar), implementando el patrón MVC (MTV en Django) con una estética y diseño enfocados al mundo Gamer.

## 2. Motor de Base de Datos Utilizado
Este proyecto está configurado para utilizar **PostgreSQL** como motor de base de datos relacional principal, gestionado a través de la librería `psycopg2-binary`.

## 3. Descripción del Modelo de Datos
El modelo de datos se estructura en dos entidades principales relacionadas mediante el ORM de Django:
* **Category:** Entidad independiente que agrupa los productos (ej. Periféricos, Monitores). Contiene un campo de nombre (`CharField`).
* **Product:** Entidad principal del catálogo. Incluye atributos como `name` (Nombre), `description` (Descripción textual), `price` (Precio decimal validado para ser mayor a 0), `stock` (Inventario), y campos para imágenes (`image` como archivo y `image_url` como enlace). 
* **Relación:** `Product` tiene una relación de muchos a uno (`ForeignKey`) con `Category`.

## 4. Rutas Principales del Módulo de Administración
El proyecto expone las siguientes rutas principales para la gestión CRUD:
* `GET /products/` : Listado completo de productos en el catálogo.
* `GET/POST /products/create/` : Renderiza y procesa el formulario para crear un nuevo producto.
* `GET/POST /products/edit/<id>/` : Renderiza y procesa el formulario para modificar un producto existente.
* `GET/POST /products/delete/<id>/` : Pantalla de confirmación y lógica de eliminación física del producto en la base de datos.

## 5. Pasos para Ejecutar el Proyecto
Para desplegar este proyecto en un entorno local, sigue estas instrucciones:

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
