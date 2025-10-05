from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import User

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
def user_profile(request,user):
    user=User.objects.get(id=user.id)
    return render(request,'users/user_profile.html')
    
        
