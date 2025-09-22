import datetime
from .models import CarBrand,CarModel,Cars,CarViews
from django.shortcuts import render
from django.http import JsonResponse
from .constants import TYPES,REGIONS,COLORS
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
    return ip
    

def main_view(request):
    print(request)
    cars=Cars.objects.all()
    brands=CarBrand.objects.all()
    context={'types':TYPES,'regions':REGIONS,'ranges':range(1900,datetime.date.today().year+1),'brands':brands,'colors':COLORS,'cars':cars}
    return render(request,'main/index.html',context=context)

def get_models(request,slug):
    try:
        brands=CarBrand.objects.get(slug=slug)
        models=brands.models.all()
        data=[{'id':m.id,'models':m.model}for m in models]
        return JsonResponse(data, safe=False)
    except CarBrand.DoesNotExist:
        return JsonResponse([], safe=False)
    
def model_detail(request,slug):
    
    car=Cars.objects.get(slug=slug)
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
    
def search(request):
    print(request)
    print("GET parameters:", request.GET)
    
    car_type = request.GET.get('type')
    region = request.GET.get('region') 
    brand = request.GET.get('brand')
    model = request.GET.get('model')
    year = request.GET.get('year')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    print(f"Type: {car_type}, Region: {region}, Brand: {brand}, Model: {model}")