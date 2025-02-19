from django.shortcuts import render
from market.forms import ItemForm

def home_view(request):
    return render(request, 'home.html')


def sell_view(request):
    return render(request, 'sell_item.html')


def sell_view(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)  # Include FILES for image uploads
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "sell_item.html", context)
