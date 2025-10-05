from django.urls import path
from .import views
app_name='chat'
urlpatterns = [
    path('chat/<str:user>/',views.chats_view,name='chats')
]
