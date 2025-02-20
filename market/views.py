from market.forms import ItemForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, ItemImage
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Access cleaned data
            username = form.cleaned_data.get('username')  # Getting the username from the cleaned data
            password = form.cleaned_data.get('password1')  # Getting the password from the cleaned data
            email = form.cleaned_data.get('email')  # Getting the email from the cleaned data
            # Do something with the cleaned data (e.g., create the user, authenticate)
            user = form.save()
            return redirect('home_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_view')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home_view')  # Redirect to home or login page after logout




def home_view(request):
    return render(request, 'home.html')


def sell_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the item first
            item = form.save()
            # Retrieve the list of uploaded images
            images = request.FILES.getlist('images')
            # Create an ItemImage for each uploaded image
            for image in images:
                ItemImage.objects.create(item=item, image=image)
            return redirect('home_view')  # or another appropriate URL
    else:
        form = ItemForm()
    context = {"form": form}
    return render(request, "sell_item.html", context)



# View to list all items
def item_list_view(request):
    items = Item.objects.all()
    return render(request, "item_list.html", {"items": items})



# View to display a single item and its images
def item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    images = ItemImage.objects.filter(item=item)
    context = {"item": item, "images": images}
    return render(request, "item_page.html", context)