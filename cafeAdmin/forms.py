from django import forms
from .models import Cafe


class CafeForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'contact_number', 'email', 'address', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }
