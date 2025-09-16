import datetime
from .models import CarBrand,CarModel,Cars
from django.shortcuts import render
from django.http import JsonResponse
from .constants import TYPES,REGIONS,COLORS

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