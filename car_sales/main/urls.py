from django.urls import path
from . import views
app_name='main'
urlpatterns = [
    path('',views.main_view,name='main'),
    path("get-models/<slug:slug>/", views.get_models, name="get_models"),
    path("search/", views.search, name="search"),
]
