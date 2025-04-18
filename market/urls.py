from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path('sell/', views.sell_view, name='sell_item'),
    path('items/', views.item_list_view, name='item_list'),  # Show all items
    path('item/<int:item_id>/', views.item_view, name='item_view'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_results, name='search_results'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    #path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('mark-sold/<int:item_id>/', views.mark_sold, name='mark_sold'),

 ]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
