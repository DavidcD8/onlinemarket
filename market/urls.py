from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home_view'),
     path('sell/', views.sell_view, name='sell_view'),

]
