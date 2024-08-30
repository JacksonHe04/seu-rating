"""
URL configuration for djangoProjectPro project.

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
from django.urls import include, path

urlpatterns = [
    # 在Django项目中，注册应用的URL配置
    # 包含管理员站点的URL模式，用于管理后台界面的访问
    path("admin/", admin.site.urls),
    # 在URL配置中引入smrWeb应用的URL模式
    path("", include("smrWeb.urls")),

]
