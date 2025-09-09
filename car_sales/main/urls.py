from django.urls import path
from . import views

urlpatterns = [
    path('',views.main_view,name='main'),
    path("get-models/<slug:slug>/", views.get_models, name="get_models")
]
