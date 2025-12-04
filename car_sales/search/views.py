from django.shortcuts import render
from django.core.paginator import Paginator
from main.models import Cars
from decimal import Decimal
from django.db.models import Q
from django.core.cache import cache

def search(request):
    print(request.GET)
    cars=Cars.objects.filter(
        available=True
    )
    query=Q()
    for param,value in request.GET.items():
        if not value:
            continue
        match param:
            case 'type':
                query&=Q(category=value)
            case 'region':
                query&=Q(region=value)
            case 'brand':
                query&=Q(brand__slug=value)
            case 'model':
                query&=Q(model__id=value)
            case 'year_min':
                query&=Q(year__gte=value)
            case 'year_max':
                query&=Q(year__lte=value)
            case 'price_min':
                try:
                    query&=Q(price__gte=Decimal(value))
                except Exception:
                    pass
            case 'price_max':
                try:
                    query&=Q(price__lte=Decimal(value))
                except Exception:
                    pass
    cars=cars.filter(query)
    print(cars)
    paginator=Paginator(cars,2)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'search/search.html',{'page_obj':page_obj})

def use(request):
    ordering=request.GET.get("ordering","id")
    cars=Cars.objects.filter(used=True).order_by(ordering)
    paginator=Paginator(cars,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'search/use.html',{'page_obj':page_obj})    

def new(request):
    cars=Cars.objects.filter(used=False).order_by('-id')
    paginator=Paginator(cars,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'search/new.html',{'page_obj':page_obj})    