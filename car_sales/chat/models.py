from django.db import models
from django.conf import settings
class GroupName(models.Model):
    group_name=models.CharField(max_length=132,unique=True)
    
    def __str__(self):
        return self.group_name
    
class GroupMessages(models.Model):
    group=models.ForeignKey(GroupName,related_name='chat_messages',on_delete=models.CASCADE)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    body=models.CharField(max_length=255)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author.username}:{self.body}"
    
    class Meta:
        ordering=['-created']