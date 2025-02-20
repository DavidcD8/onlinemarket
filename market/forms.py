from django import forms
from django.contrib.auth.models import User
from .models import Item, ItemImage
  
 

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'condition']

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']
