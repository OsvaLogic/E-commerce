# Osva.Logic - E-Commerce Gamer (Headless API Enterprise)

## 1. Arquitectura y Propósito
Osva.Logic es un backend de E-commerce diseñado bajo una arquitectura **Headless**. Se ha construido como una API RESTful utilizando Django REST Framework (DRF), separando completamente la lógica de negocio y acceso a datos de la interfaz de usuario.
Esta arquitectura está preparada para escalar, implementando autenticación segura por tokens (JWT) y procesamiento asíncrono de tareas pesadas en segundo plano.

## 2. Stack Tecnológico
* **Framework Principal:** Django & Django REST Framework (DRF)
* **Base de Datos Transaccional:** PostgreSQL 14
* **Autenticación:** SimpleJWT (JSON Web Tokens)
* **Caché y Broker de Mensajes:** Redis
* **Procesamiento Asíncrono:** Celery (Ej: envío de correos, integraciones)
* **Infraestructura:** Docker & Docker Compose

## 3. Descripción del Modelo de Datos
El modelo de datos gestiona el ciclo de vida completo de un e-commerce:
* **Category:** Agrupación de productos (ej. Periféricos, Monitores).
* **Product:** Catálogo principal con `stock`, `price`, e imágenes. Relacionado (N:1) a Category.
* **Order & OrderItem:** Registro transaccional de compras con historial de productos, cantidad, precio fijo en el momento de compra y total. Manejo seguro con transacciones atómicas (`select_for_update`).

## 4. Endpoints de la API (Rutas Principales)
La API está habilitada para CORS (Next.js / React) y responde en formato JSON:

### Autenticación (JWT)
* `POST /api/token/` : Envía credenciales (`username`, `password`) y recibe tokens de acceso y refresco.
* `POST /api/token/refresh/` : Renueva un token de acceso vencido.

### Catálogo (Público / Admin)
* `GET /api/products/` : Lista el catálogo completo (Soporta búsqueda `?q=termino`).
* `GET /api/products/{id}/` : Detalle de un producto específico.
* `POST /api/products/` : Crear producto (Requiere autenticación de Staff/Admin).

### Transacciones (Requiere Autenticación)
* `POST /api/checkout/` : Procesa el carrito de compras, resta stock, crea la orden y dispara tareas en segundo plano.
  * **Payload esperado:** `{"cart": {"id_producto": cantidad, "id_producto2": cantidad}}`
  * **Header:** `Authorization: Bearer <access_token>`

## 5. Despliegue y Ejecución Rápida (Docker)
El proyecto está completamente contenerizado, lo que significa que no necesitas instalar PostgreSQL o Redis en tu máquina anfitriona.

Asegúrate de tener Docker Desktop instalado y ejecuta:

```bash
# Construir imágenes y levantar todos los servicios (Django, DB, Redis, Celery)
docker-compose up --build
