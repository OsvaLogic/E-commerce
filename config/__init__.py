# Esto asegurará que Celery siempre se importe cuando Django inicie,
# de forma que el decorador @shared_task funcione correctamente.
from .celery import app as celery_app

__all__ = ('celery_app',)