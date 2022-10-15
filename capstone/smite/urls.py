from django.urls import path

from . import views

app_name = 'smite'
urlpatterns = [
    path('', views.index, name='index'),
    path('gods/', views.gods, name='gods'),
    path('items/', views.items, name='items'),
    path('player/<str:player>/<str:name>/', views.player, name='player'),
    path('search_player/',
         views.search_player, name='search_player'),
    path('search_results/<str:player>/',
         views.search_results, name='search_results'),
    path('god/<str:r_Name>/', views.god, name='god'),
    path('match/<int:match>/', views.get_match, name='get_match'),
    path('skins/<str:name>/<int:id>/', views.skins, name='skins'),
    path('checkapi/', views.check, name='check_api'),
]
