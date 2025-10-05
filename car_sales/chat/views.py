from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GroupName

@login_required
def chats_view(request):
    return render(request,'chat/chats.html')
