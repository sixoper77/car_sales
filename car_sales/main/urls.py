from django.urls import path
from . import views
app_name='main'
urlpatterns = [
    path('',views.main_view,name='main'),
    path("get-models/<slug:slug>/", views.get_models, name="get_models"),
    path("detail/<slug:slug>/", views.model_detail, name="detail"),
    path('like/<slug:slug>/',views.likes,name='like'),
    
]
