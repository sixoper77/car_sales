from django.urls import path
from . import views
app_name='sale'
urlpatterns = [
    path('add-car',views.add_car,name='add-car'),
    path('get-models/<slug:slug>/',views.get_models,name='get-models')
]
