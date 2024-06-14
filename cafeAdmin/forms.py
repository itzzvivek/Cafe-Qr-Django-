from django import forms
from .models import Cafe


class CafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'contact_number', 'address', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }
