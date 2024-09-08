# smrWeb/urls.py
# 主应用路由管理
from django.urls import path
from . import views

urlpatterns = [
    # 进入登录页面
    path('', views.log_in, name='log_in'),
    # 登录页面
    path('login/', views.log_in, name='log_in'),
    # 登录检查
    path('logcheck/', views.log_check, name='log_check'),
    # 首页
    path('home/', views.home_page, name='homepage'),
    # 音乐专辑
    path('albums/', views.albums_page, name='albums'),
    # 发现音乐
    path('searchmusic/', views.search_music, name='search_music'),
    # 音乐人
    path('musicians/', views.musicians_page, name='musicians'),
    # 帮助
    path('help/', views.help_page, name='help'),
    # 关于
    path('about/', views.about_page, name='about'),
    # 音乐人结果
    path('musicianresult/', views.musician_result, name='musician_result'),
    # 专辑搜索结果
    path('albumresult/', views.album_result_search, name='album_result_search'),
    # 从音乐人页面进入专辑的结果
    path('albumresult/<int:album_id>/', views.album_result, name='album_result'),
]
