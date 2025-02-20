from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('sell/', views.sell_view, name='sell_view'),
    path('items/', views.item_list_view, name='item_list_view'),  # Show all items
    path('item/<int:item_id>/', views.item_view, name='item_view'),  # Show item details
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)