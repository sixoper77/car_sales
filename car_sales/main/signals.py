from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Cars


@receiver([post_save,post_delete],sender=Cars)
def invalidate_cars_cache(sender,instance,**kwargs):
    cache.delete('car_list')
    print(f'кеш инвалидирован для {instance}')