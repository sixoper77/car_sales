from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    image=models.ImageField(upload_to='users_image',blank=True,null=True)
    last_active=models.DateTimeField(null=True,blank=True)
    
    class Meta:
        db_table='user'
        
    def __str__(self):
        return self.get_username()