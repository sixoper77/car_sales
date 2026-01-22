from django import forms
from main.models import Cars


class AddCarform(forms.ModelForm):
    class Meta:
        model = Cars
        fields = [
            "category",
            "brand",
            "model",
            "region",
            "price",
            "color",
            "discount",
            "gearbox",
            "mileage",
            "air_conditioner",
            "year",
            "used",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": "dropdown", "id": "typeDropdown"}),
            "brand": forms.Select(attrs={"class": "dropdown", "id": "brandDropdown"}),
            "gearbox": forms.Select(
                attrs={"class": "dropdown", "id": "gearboxDropdown"}
            ),
            "air_conditioner": forms.Select(
                attrs={"class": "dropdown", "id": "air_conditionerDropdown"}
            ),
            "used": forms.Select(attrs={"class": "dropdown", "id": "usedDropdown"}),
            "mileage": forms.NumberInput(
                attrs={"class": "price-input", "id": "mileageDropdown"}
            ),
            "model": forms.Select(attrs={"class": "dropdown", "id": "modelDropdown"}),
            "year": forms.Select(attrs={"class": "dropdown", "id": "yearDropdown"}),
            "color": forms.Select(attrs={"class": "dropdown"}),
            "region": forms.Select(attrs={"class": "dropdown", "id": "regionDropdown"}),
            "price": forms.NumberInput(attrs={"class": "price-inputs"}),
            "discount": forms.NumberInput(attrs={"class": "discount-input"}),
        }
