from django import forms
from .models import Item, ItemImage
from django.forms import inlineformset_factory



class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']

