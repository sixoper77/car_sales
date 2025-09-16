from django import forms
from main.models import Cars
from main.constants import COLORS
class AddCarform(forms.ModelForm):
    class Meta:
        model=Cars
        fields=['category','brand','model','region','price','color','discount','image','year']
        widgets={
            'category':forms.Select(attrs={'class':'dropdown','id':'typeDropdown'}),
            'brand':forms.Select(attrs={'class':'dropdown','id':'brandDropdown'}),
            'model':forms.Select(attrs={'class':'dropdown','id':'modelDropdown'}),
            'year':forms.Select(attrs={'class': 'dropdown', 'id': 'yearDropdown'}),
            'color':forms.Select(attrs={'class':'dropdown'}),  
            'region':forms.Select(attrs={'class':'dropdown','id':'regionDropdown'}),
            'price':forms.NumberInput(attrs={'class':'price-inputs'}),
            'discount': forms.NumberInput(attrs={'class': 'discount-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'image-input'}),
        }