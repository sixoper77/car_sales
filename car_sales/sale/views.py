import datetime
from django.shortcuts import redirect, render
from main.models import CarBrand,CarImage, Cars
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from . forms import AddCarform
from django.utils.text import slugify
from django.contrib import messages

@login_required
def add_car(request):
    print(request)
    if request.method=='POST':
        form=AddCarform(request.POST)
        if form.is_valid():
            car=form.save(commit=False)
            car.owner=request.user
            car.save()
            car.slug=slugify(f'{car.brand}-{car.model}-{car.id}')
            images=request.FILES.getlist('images')
            print(images)
            if len(images)>15:
                images=images[:15]
            for ind , image in enumerate(images):
                print(f'Сохраняю фото:{ind+1}')
                CarImage.objects.create(
                    car=car,
                    image=image
                )
                if ind==0:
                    car.image=image
                    car.save(update_fields=['image','slug'])
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
    
def update_ad(request,ad):
    car=Cars.objects.select_related('owner').prefetch_related('images').get(id=ad,owner=request.user)
    print(request.POST)
    if request.method=='POST':
        form=AddCarform(request.POST,instance=car)
        if form.is_valid():
            car=form.save(commit=False)
            car.owner=request.user
            car.slug=slugify(f'{car.brand}-{car.model}-{car.id}')
            car.save() 
            new_images=request.FILES.getlist('images')
            print(new_images)
            delete_images=request.POST.getlist('delete_images')
            if delete_images:
                CarImage.objects.filter(id__in=delete_images,car=car).delete()
            if new_images:
                exist_count=15-car.images.count()
                if exist_count>0:
                    new_images=new_images[:exist_count]
                for idx,img in enumerate(new_images):
                    CarImage.objects.create(car=car,image=img)
                if car.image!=car.images.first():
                    first=car.images.first()
                    car.image=first.image
                    car.save(update_fields=['image'])    
            
            messages.success(request,'Оголошення успішно оновленно')
            return redirect('users:ads')
        
        print(form.errors)
    else:
        form=AddCarform(instance=car)
    exist_img=car.images.all()
    return render(request,'sale/update.html',{'form':form,'car':car,'exist_img':exist_img,'ranges': range(1900, datetime.date.today().year + 1)})        
                
                    
                
            
   
    
    
    
    

