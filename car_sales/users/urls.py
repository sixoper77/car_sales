from django.urls import path
from . import views

app_name='users'
urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('profile_/<str:username>/',views.user_profile,name='profile_'),
    path('ads/',views.get_my_ads,name='ads'),
    path('delete/<int:id>/',views.delete_ad,name='delete'),
    path('del_like/<slug:slug>/',views.delete_like,name='del_like'),
    path('my_choise/',views.get_my_choise,name='my_choise'),
]
