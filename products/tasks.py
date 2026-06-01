from celery import shared_task
from .models import Order
import time

@shared_task
def send_confirmation_email(order_id):
    """
    Esta tarea se ejecutará en el contenedor de Celery sin bloquear 
    la respuesta HTTP de la API al usuario.
    """
    try:
        order = Order.objects.get(id=order_id)
        # Simulamos un retraso como si estuviéramos conectando a un servicio externo (ej. Klaviyo/SendGrid)
        time.sleep(2)
        print(f"[CELERY WORKER] -> Correo de confirmación enviado exitosamente al usuario {order.user.username} para la Orden #{order.id} con total de ${order.total}.")
        return True
    except Order.DoesNotExist:
        return False