from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='clp_format')
def clp_format(value):
    # Actúa como puente: usa el formato nativo de Django automáticamente
    return intcomma(value)