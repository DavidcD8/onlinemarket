from .models import Profile
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

 
 

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    number = forms.IntegerField(label="Phone Number")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'number']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



 
class ProfileForm(forms.ModelForm):
    # Explicitly include the 'email' field to allow the user to update it
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['name', 'number', 'email']  # Include 'email' in the form fields

    def __init__(self, *args, **kwargs):
        # Pass the initial email value from the associated User model
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        # Save the form data
        profile = super().save(commit=False)
        
        # Update the associated User's email field
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        
        # Now save the profile instance
        profile.save()
        
        return profile
