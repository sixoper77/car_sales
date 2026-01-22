from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    path("search-car/", views.search, name="search-car"),
    path("used-cars/", views.use, name="used-cars"),
    path("news-cars/", views.new, name="news-cars"),
]
