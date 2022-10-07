from django.urls import path

from . import views

app_name = 'smite'
urlpatterns = [
    path('', views.index, name='index'),
    path('gods/', views.gods, name='gods'),
    path('items/', views.items, name='items'),
    path('player/', views.player, name='player'),
    path('god/<str:r_Name>/', views.god, name='god'),
]
