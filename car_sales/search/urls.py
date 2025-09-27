from django.urls import path
from . import views

urlpatterns = [
    path('search-car/',views.search,name='search-car')
]




app_name='search'