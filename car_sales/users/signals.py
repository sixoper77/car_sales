from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.files.base import ContentFile
import requests

@receiver(user_signed_up)
def populate_profile(sender,request,user,**kwargs):
    social_account=SocialAccount.objects.filter(
        user=user,
        provider='google',
        
    ).first()
    if social_account:
        data=social_account.extra_data
        user.first_name=data.get('given_name','')
        user.last_name=data.get('family_name','')
        image=data.get('picture')
        if image:
            try:
                req=requests.get(image)
                if req.status_code==200:
                    user.image.save(
                        f'{user.id}_avatar.jpg',
                        ContentFile(req.content),
                        save=False
                    )
            except:
                pass
        user.save()