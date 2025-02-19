from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home_view, name='home_view'),
    path('sell/', views.sell_view, name='sell_view'),
    path('items/', views.item_list_view, name='item_list_view'),  # Show all items
    path('item/<int:item_id>/', views.item_view, name='item_view'),  # Show item details
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)