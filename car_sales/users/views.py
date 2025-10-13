from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main.models import Cars
from .forms import ProfileForm
from .models import User
from django.core.paginator import Paginator

@login_required
def profile(request):
    if request.method=='POST':
        form=ProfileForm(data=request.POST,instance=request.user,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile was changed')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form=ProfileForm(instance=request.user)
    return render(request,'users/profile.html',{'form':form})
    
@login_required
def user_profile(request,username):
    user=User.objects.get(username=username)
    
    return render(request,'users/user_profile.html',{'user':user})


@login_required
def get_my_ads(request):
    cars=Cars.objects.filter(owner=request.user).order_by('-id')
    paginator=Paginator(cars,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'users/ads.html',{'page_obj':page_obj})
    

@login_required
def delete_ad(request,id):
    car=get_object_or_404(Cars,id=id)
    car_id=car.id
    car.delete()
    messages.success(request,f'Оголошення номер {car_id} видалено!')
    return redirect('users:ads')