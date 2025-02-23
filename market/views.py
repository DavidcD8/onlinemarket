from market.forms import ItemForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, ItemImage
from .forms import UserRegisterForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile




# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in new user
            return redirect('home')

    else:
        form = UserRegisterForm()  # Ensure custom form is being instantiated

    return render(request, 'registration/register.html', {'form': form})  # Render form properly




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



# View for profile page
@login_required
def profile_view(request):
    # Try to get the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # If the form is submitted, process the data
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to avoid resubmitting the form
    else:
        # If the form is not submitted, display the current profile information
        form = ProfileForm(instance=profile)


    context = {
        'current_page': 'profile',
        'form': form,
        'profile': profile,
        'items': Item.objects.filter(seller=request.user, is_sold=False)
    }
    context['sold_items'] = Item.objects.filter(seller=request.user, is_sold=True)
    print("Sold items:", context['sold_items'])  # Debugging line

    return render(request, 'profile.html', context)





@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'form': form})




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
    items = Item.objects.filter(is_sold=False)
    return render(request, "item_list.html", {"items": items})




# View to display a single item and its images
def item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    images = ItemImage.objects.filter(item=item)
    profile = item.seller.profile  # Access the profile from the seller
    context = {
        "item": item,
        "images": images,
        "profile": profile,  # Add the profile to the context

    }
    return render(request, "item_page.html", context)




@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.seller != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_view', item_id=item_id)
    else:
        form = ItemForm(instance=item)
    return render(request, "edit_item_page.html", {"form": form, "item": item})


# View to mark an item as sold
@login_required
def mark_sold(request, item_id):
    item = get_object_or_404(Item, id=item_id, seller=request.user)
    item.is_sold = True
    item.save()
    return redirect('profile')  # Redirect to profile after marking as sold

