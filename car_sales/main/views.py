import datetime
from .models import CarBrand,CarModel,Cars,CarViews, Category
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .constants import TYPES,REGIONS,COLORS
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.core.cache import cache
from django.shortcuts import get_object_or_404


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

    
def main_view(request):
    types=cache.get('types')
    if not types:
        types=list(Category.objects.values_list('id','name'))
        cache.set('types',types,60*5)
    cars=cache.get('car_list')
    print(cars)
    if not cars:
        cars=list(Cars.objects.select_related('owner','brand','model','category').prefetch_related('likes').order_by('-id'))
        cache.set('car_list',cars,60*2)
    paginator=Paginator(cars,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    brands=CarBrand.objects.all()

    context={'types':types,'regions':REGIONS,'ranges':range(1900,datetime.date.today().year+1),'brands':brands,'colors':COLORS,'page_obj':page_obj}
    return render(request,'main/index.html',context=context)

def get_models(request,slug):
    try:
        brands=CarBrand.objects.prefetch_related('models').get(slug=slug)
        models=brands.models.all()
        data=[{'id':m.id,'models':m.model}for m in models]
        return JsonResponse(data, safe=False)
    except CarBrand.DoesNotExist:
        return JsonResponse([], safe=False)
    
def model_detail(request,slug):
    car=Cars.objects.select_related(
        'owner','category','brand','model'
        ).prefetch_related('likes').get(slug=slug)
    ip=get_client_ip(request)
    if request.user.is_authenticated:
        exist=CarViews.objects.filter(car=car).filter(
            Q(user=request.user)|Q(ip_address=ip)
        ).exists()
    else:
        exist=CarViews.objects.filter(
            car=car,ip_address=ip
        ).exists()
    if not exist:
        CarViews.objects.create(
            car=car,
            user=request.user if request.user.is_authenticated else None,
            ip_address=ip,
        )
    return render(request,'main/detail.html',{'car':car})
    
def likes(request,slug):
    ad=get_object_or_404(Cars,slug=slug)
    if request.user in ad.likes.all():
        ad.likes.remove(request.user)
    else:
        ad.likes.add(request.user)
    return redirect('main:detail',slug=ad.slug)