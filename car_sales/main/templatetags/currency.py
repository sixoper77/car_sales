from django import template
from scheduler.models import ExchangeRate

register=template.Library()

@register.filter
def usd_to_uah(value):
    try:
        rate=ExchangeRate.objects.get(currency='USD').rate
        return round(value*rate,2)
    except ExchangeRate.DoesNotExist:
        return value