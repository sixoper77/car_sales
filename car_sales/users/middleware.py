from .models import User
from django.utils import timezone

class UpdateUserLastActivityMiddelware:
    def __init__(self,get_response):
        self.get_response=get_response
        
    def __call__(self, request):
        response=self.get_response(request)
        
        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_active=timezone.now())
        return response