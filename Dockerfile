# Usamos una imagen oficial de Python ligera
FROM python:3.10-slim

# Establecemos variables de entorno para que Python no genere archivos .pyc y la salida sea directa
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . /app/