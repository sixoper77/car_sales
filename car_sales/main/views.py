import datetime
from .models import CarBrand,CarModel
from django.shortcuts import render
from django.http import JsonResponse
from .constants import TYPES,REGIONS

def main_view(request):
    brands=CarBrand.objects.all()
    context={'types':TYPES,'regions':REGIONS,'ranges':range(1900,datetime.date.today().year+1),'brands':brands}
    return render(request,'main/index.html',context=context)

def get_models(request,slug):
    try:
        brands=CarBrand.objects.get(slug=slug)
        models=brands.models.all()
        data=[{'id':m.id,'models':m.model}for m in models]
        return JsonResponse(data, safe=False)
    except CarBrand.DoesNotExist:
        return JsonResponse([], safe=False)