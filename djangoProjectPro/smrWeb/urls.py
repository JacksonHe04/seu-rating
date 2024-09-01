# smrWeb/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # home_page
    path('', views.log_in, name='log_in'),
    path('home/', views.home_page, name='homepage'),
    # log_in
    path('login/', views.log_in, name='log_in'),
    # album
    path('albums/', views.albums_page, name='albums'),
    # search_music
    path('searchmusic/', views.search_music, name='search_music'),
    # musician
    path('musicians/', views.musicians_page, name='musicians'),
    # service_page
    path('help/', views.help_page, name='help'),
    # more_page
    path('about/', views.about_page, name='about'),

    path('logcheck/', views.log_check, name='log_check'),

    # musician_result
    path('musicianresult/', views.musician_result, name='musician_result'),

    # album_result
    path('albumresult/', views.album_result, name='album_result'),

]
