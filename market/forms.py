from django import forms
from django.contrib.auth.models import User
from .models import Item, ItemImage
  
 

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'condition']  # Explicitly include all fields except 'user'

    def save(self, commit=True, user=None):
        # Make sure that the user is set from the current logged-in user
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']
