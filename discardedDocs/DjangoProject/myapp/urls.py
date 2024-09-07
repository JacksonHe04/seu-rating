from django.urls import path
from . import views
# 可能没用
urlpatterns = [
    # 增加子路由login_view
    path('login', views.login_view, name='login'),
    path('check_login/', views.check_login, name='check_login'),  # 新增这一行
    path('add_book/', views.add_book, name='add_book'),
    path('list_books/', views.list_books, name='list_books'),
    path('update-book/<int:book_id>/', views.update_book, name='update_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('home/', views.home, name='home'),  # 添加这一行

]
