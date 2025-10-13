from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Cars,CarBrand
from django.core.cache.utils import make_template_fragment_key

@receiver([post_save,post_delete],sender=Cars)
def invalidate_cars_cache(sender,instance,**kwargs):
    detail=cache.delete(make_template_fragment_key('car_detail',[instance.id]))
    print(f'Кеш удален для детального раздела машины {instance.id} : {detail}')
    if instance.used:
        used=cache.delete(make_template_fragment_key('car_use',[instance.id]))
        print(f'Кеш удален для использованой машины {instance.id} : {used}')
    else:
        new=cache.delete(make_template_fragment_key('car_new',[instance.id]))
        print(f'Кеш удален для новой машины {instance.id} : {new}')
    cache.delete('car_list')
    print(f'кеш инвалидирован при сохранении  {instance.id}')
    
