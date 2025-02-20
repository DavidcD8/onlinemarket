from market.forms import ItemForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, ItemImage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# View for home page
def home(request):
    return render(request, 'home.html', {'current_page': 'home'})
 


# View to search for items
def search_results(request):
    query = request.GET.get("query")
    results = Item.objects.filter(name__icontains=query)
    return render( request, "search_results.html", {"results": results, "query": query})



# View to sell an item
@login_required
def sell_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # Directly assign request.user
            item.seller = request.user  
            item.save()

            # Save images related to the item
            images = request.FILES.getlist('images')
            for image in images:
                ItemImage.objects.create(item=item, image=image)

            return redirect('home')
    else:
        form = ItemForm()

    return render(request, "sell_item.html", {"form": form})



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