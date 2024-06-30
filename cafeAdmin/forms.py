from django import forms
from .models import Cafe
from core.models import Category, MenuItem


class CafeRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cafe
        fields = ['cafe_name', 'contact_number', 'email', 'address', 'slug']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = 'name'

    def __init__(self, *args, **kwargs):
        cafe = kwargs.pop('cafe', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        if cafe:
            self.fields['name'].queryset = Category.objects.filter(cafe=cafe)


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'min_price', 'max_price', 'category']

    def __init__(self, *args, **kwargs):
        cafe= kwargs.pop('cafe', None)
        super(MenuItemForm, self).__init__(*args, **kwargs)
        if cafe:
            self.fields['category'].queryset = MenuItem.objects.filter(cafe=cafe)




