from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from main.models import Cars

from .forms import ProfileForm
from .models import User


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            data=request.POST, instance=request.user, files=request.FILES
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile was changed")
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "users/profile.html", {"form": form})


@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)

    return render(request, "users/user_profile.html", {"user": user})


@login_required
def get_my_ads(request):
    cars = Cars.objects.filter(owner=request.user).order_by("-id")
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "users/ads.html", {"page_obj": page_obj})


@login_required
def delete_ad(request, id):
    car = get_object_or_404(Cars, id=id)
    car_id = car.id
    car.delete()
    messages.success(request, f"Оголошення номер {car_id} видалено!")
    return redirect("users:ads")


@login_required
def get_my_choise(request):
    cars = Cars.objects.filter(likes=request.user)
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "users/my_choise.html", {"page_obj": page_obj})


def delete_like(request, slug):
    car = get_object_or_404(Cars, slug=slug)
    car.likes.remove(request.user)
    return redirect("users:my_choise")
