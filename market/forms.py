from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Item, ItemImage
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']
