from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path("chat/", views.chats_view, name="chats"),
    path("chat/<str:user>/", views.chats_view, name="chats"),
    path("find/", views.find_chat, name="find"),
]
