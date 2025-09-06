import datetime
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from . constants import *

class Category(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=255,unique=True)
    
    class Meta:
        ordering=['name']
        indexes=[models.Index(fields=['name'])]
        verbose_name='category'
        verbose_name_plural='categories'
        
    def get_absolute_url(self):
        return reverse("main:by_categories", args=[self.slug])
    
    def __str__(self):
        return self.name
    
class Cars(models.Model):
    category=models.ForeignKey(Category,related_name='cars',on_delete=models.CASCADE)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='cars',on_delete=models.CASCADE)
    year=models.PositiveIntegerField(validators=[MinValueValidator(1900),MaxValueValidator(datetime.date.today().year)],verbose_name='Рік випуску')
    type=models.CharField(max_length=255,choices=TYPES,verbose_name='Тип машини')
    slug=models.SlugField(max_length=255)
    brand=models.CharField(max_length=255)
    model=models.CharField(max_length=255)
    region=models.CharField(max_length=255,choices=REGIONS,verbose_name='Область')
    price=models.DecimalField(max_digits=15,decimal_places=2)
    avialeble=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    discount=models.DecimalField(default=0.00,max_digits=4,decimal_places=2)
    image=models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    
    class Meta:
        ordering=['name']
        indexes=[models.Index(fields=['id','slug']),
                 models.Index(fields=['name']),
                 models.Index(fields=['-created'])]
    def __str__(self):
        return self.model
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.slug])
    
    def get_absolute_price(self):
        if self.discount:
            return round(self.price-self.price*self.discount/100,2)
        return self.price
    
    
    