import os
from celery import Celery

# Establece el módulo de ajustes de Django por defecto para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Carga la configuración de celery desde los settings de Django
# El namespace='CELERY' indica que todas las variables en settings.py 
# relacionadas con celery deben empezar con CELERY_ (ej: CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Busca y descubre automáticamente tareas en los archivos 'tasks.py' 
# de todas tus aplicaciones de Django (ej. products/tasks.py)
app.autodiscover_tasks()