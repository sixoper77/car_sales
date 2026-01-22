import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from main.models import CarBrand, CarImage, Cars

from .forms import AddCarform


@login_required
def add_car(request):
    if request.method == "POST":
        form = AddCarform(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            images = request.FILES.getlist("images")[:15]
            car.save()
            if images:
                first_image = images[0]
                car.image.save(
                    first_image.name, ContentFile(first_image.read()), save=True
                )
                first_image.seek(0)
            for image in images:
                image.seek(0)
                CarImage.objects.create(
                    car=car, image=ContentFile(image.read(), name=image.name)
                )
            car.slug = slugify(f"{car.brand}-{car.model}-{car.id}")
            car.save(update_fields=["slug"])
            return redirect("main:main")
    else:
        form = AddCarform()
    return render(
        request,
        "sale/sale.html",
        context={"form": form, "ranges": range(1900, datetime.date.today().year + 1)},
    )


def get_models(request, slug):
    try:
        brands = CarBrand.objects.get(slug=slug)
        models = brands.models.all()
        data = [{"id": m.id, "models": m.model} for m in models]
        return JsonResponse(data, safe=False)
    except CarBrand.DoesNotExist:
        return JsonResponse([], safe=False)


def update_ad(request, ad):
    car = (
        Cars.objects.select_related("owner")
        .prefetch_related("images")
        .get(id=ad, owner=request.user)
    )
    print(request.POST)
    if request.method == "POST":
        form = AddCarform(request.POST, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.slug = slugify(f"{car.brand}-{car.model}-{car.id}")
            car.save()
            new_images = request.FILES.getlist("images")
            print(new_images)
            delete_images = request.POST.getlist("delete_images")
            if delete_images:
                CarImage.objects.filter(id__in=delete_images, car=car).delete()
            if new_images:
                exist_count = 15 - car.images.count()
                if exist_count > 0:
                    new_images = new_images[:exist_count]
                for idx, img in enumerate(new_images):
                    CarImage.objects.create(car=car, image=img)
                if car.image != car.images.first():
                    first = car.images.first()
                    car.image = first.image
                    car.save(update_fields=["image"])

            messages.success(request, "Оголошення успішно оновленно")
            return redirect("users:ads")

        print(form.errors)
    else:
        form = AddCarform(instance=car)
    exist_img = car.images.all()
    return render(
        request,
        "sale/update.html",
        {
            "form": form,
            "car": car,
            "exist_img": exist_img,
            "ranges": range(1900, datetime.date.today().year + 1),
        },
    )
