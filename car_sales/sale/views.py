import datetime
from django.shortcuts import redirect, render
from main.models import CarBrand
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . forms import AddCarform
from django.utils.text import slugify

@login_required
def add_car(request):
    print(request)
    if request.method=='POST':
        form=AddCarform(request.POST,request.FILES)
        if form.is_valid():
            car=form.save(commit=False)
            car.owner=request.user
            car.save()
            car.slug=slugify(f'{car.brand}-{car.model}-{car.id}')
            car.save(update_fields=['slug'])
            return redirect('main:main')
    else:
        form=AddCarform()
    return render(request,'sale/sale.html',context={'form':form,'ranges':range(1900,datetime.date.today().year+1)})



def get_models(request,slug):
    try:
        brands=CarBrand.objects.get(slug=slug)
        models=brands.models.all()
        data=[{'id':m.id,'models':m.model}for m in models]
        return JsonResponse(data, safe=False)
    except CarBrand.DoesNotExist:
        return JsonResponse([], safe=False)
    

