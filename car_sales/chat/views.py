from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from .models import Message
from django.db.models import Q,Subquery,OuterRef
from django.utils import timezone

@login_required
def chats_view(request, user=None):
    users = User.objects.exclude(id=request.user.id)
    chats=[]
    chat_user=[]
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
        
        if last_message:  
            user_last_messages.append({
                'user': usr,
                'last_message': last_message
            })
   
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp,
        reverse=True
    )
    
    return render(request, 'chat/chats.html', context={
        'target_user': user,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'chat_user':chat_user
    })
    
@login_required
def find_chat(request):
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'results': []})
    last_msg_subquery = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=OuterRef('pk'))) |
        (Q(recipient=request.user) & Q(sender=OuterRef('pk')))
    ).order_by('-timestamp')
    users = User.objects.filter(
        username__icontains=username
    ).filter(
        Q(sent_message__recipient=request.user) | 
        Q(recived_message__sender=request.user)
    ).distinct().annotate(
        last_msg_body=Subquery(last_msg_subquery.values('body')[:1]),
        last_msg_time=Subquery(last_msg_subquery.values('timestamp')[:1]),
        last_msg_sender_id=Subquery(last_msg_subquery.values('sender')[:1])
    ).order_by('-last_msg_time')

    results = []
    for usr in users:
        if not usr.last_msg_time:
            continue

        results.append({
            'username': usr.username,
            'image_url': usr.image.url if usr.image else None,
            'last_message': usr.last_msg_body,
            'timestamp': usr.last_msg_time.strftime('%H:%M'),
            'is_own': usr.last_msg_sender_id == request.user.id, 
            'chat_url': f'/chat/chat/{usr.username}/'
        })
    
    return JsonResponse({'results': results})
    