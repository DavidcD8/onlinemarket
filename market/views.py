from market.forms import ItemForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, ItemImage

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