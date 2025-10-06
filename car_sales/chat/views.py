from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import Message
from django.db.models import Q
from django.utils import timezone

@login_required
def chats_view(request, user=None):
    users = User.objects.exclude(id=request.user.id)
    chats=[]
    if user:
        chat_user=get_object_or_404(User,username=user)
        chats = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient__username=user)) |
            (Q(recipient=request.user) & Q(sender__username=user)) 
        )
        chats = chats.order_by('timestamp')
    
    user_last_messages = []
    for usr in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=usr)) |
            (Q(recipient=request.user) & Q(sender=usr))
        ).order_by('-timestamp').first()
        
        if last_message:  # Додаємо тільки якщо є повідомлення
            user_last_messages.append({
                'user': usr,
                'last_message': last_message
            })
    
    # Сортування: спочатку ті, у кого є повідомлення
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp,
        reverse=True
    )
    
    return render(request, 'chat/chats.html', context={
        'user': user,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'chat_user':chat_user
    })