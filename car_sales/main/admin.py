from django.contrib import admin
from . models import Category,Cars,CarImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
    
    
class ProductImageLine(admin.TabularInline):
    model=CarImage
    extra=15
    
@admin.register(Cars)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['model','slug','price','year','brand','region','model','price','available','updated','created','discount']
    list_filter=['available','created','updated']
    list_editable=['price','available','discount']
    prepopulated_fields={'slug':('model',)}
    inlines=[ProductImageLine]