"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
# 导入视图views
from ..myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 映射URL路径' books/'到myapp应用的urls模块，实现应用内URL的包含
    path('books/', include('myapp.urls')),
    path('home/', views.home, name='home'),  # 添加这一行
    path('login', views.login_view, name='login'),
]
