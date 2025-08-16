from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_list, name='music_list'),
    path('download/<path:filename>/', views.download_music, name='download_music'),
    path('favorite/<path:filename>/', views.toggle_favorite, name='toggle_favorite'),  
    path('activity/', views.user_activity, name='user_activity'),  
    path('search-users/', views.search_users, name='search_users'),
]
