# tienda/templatetags/cyber_filtros.py
from django import template

register = template.Library()


@register.filter
def puntos(value):
    """
    Convierte un número agregando puntos como separador de miles.
    Ejemplo: 1500000 -> 1.500.000
    """
    try:
        # Formatea con comas estándar de Python y luego las cambia por puntos
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
