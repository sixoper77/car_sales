from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User
class ProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=(
            "image",
            "first_name",
            "last_name",
            "username",
            "email"
        )
        image=forms.ImageField(required=False)
        first_name=forms.CharField()
        last_name=forms.CharField()
        username=forms.CharField()
        email=forms.EmailField()