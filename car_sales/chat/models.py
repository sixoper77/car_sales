from django.db import models
from django.conf import settings

class Message(models.Model):
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sent_message',on_delete=models.CASCADE)
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='recived_message',on_delete=models.CASCADE)
    body=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['timestamp']
        
    def __str__(self):
        return f'{self.sender}-{self.recipient}-{self.body}'