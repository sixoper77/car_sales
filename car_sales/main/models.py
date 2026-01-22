import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .constants import *


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("main:by_categories", args=[self.slug])

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    brand = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["brand"]
        indexes = [models.Index(fields=["brand"])]
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.brand


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, related_name="models", on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ["model"]
        indexes = [models.Index(fields=["model"])]
        verbose_name = "model"
        verbose_name_plural = "model"

    def __str__(self):
        return self.model


class Cars(models.Model):
    category = models.ForeignKey(
        Category, related_name="cars", on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="cars", on_delete=models.CASCADE
    )
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year),
        ],
        verbose_name="Рік випуску",
    )
    used = models.BooleanField(
        choices=[(True, "Так"), (False, "Ні")], null=True, blank=True
    )
    mileage = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True
    )
    air_conditioner = models.CharField(
        choices=CONDITIONERS, verbose_name="Кондиционеры", null=True, blank=True
    )
    gearbox = models.CharField(
        choices=GEARBOX, verbose_name="Коробки передач", null=True, blank=True
    )
    slug = models.SlugField(max_length=255)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likes", blank=True
    )
    brand = models.ForeignKey(CarBrand, related_name="cars", on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, related_name="cars", on_delete=models.CASCADE)
    region = models.CharField(max_length=255, choices=REGIONS, verbose_name="Область")
    price = models.DecimalField(max_digits=15, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    color = models.CharField(
        max_length=255, choices=COLORS, verbose_name="Кольори", blank=True, null=True
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)

    class Meta:
        ordering = ["model"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["model"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"{self.model.model}"

    def get_absolute_url(self):
        return reverse("main:detail", args=[self.slug])

    def get_absolute_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

    # def total_likes(self):
    #     return self.likes.count()


class CarViews(models.Model):
    car = models.ForeignKey(Cars, related_name="views", on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    viewed_at = models.DateTimeField(default=timezone.now)


class CarImage(models.Model):
    car = models.ForeignKey(Cars, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)

    def __str__(self):
        return f"{self.car.model}-{self.image.name}"
