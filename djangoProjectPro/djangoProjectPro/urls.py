# djangoProjectPro/djangoProjectPro/urls.py
# Django 项目路由管理，主要的路由管理请移步 smrWeb/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # 进入管理员站点，用于管理后台界面的访问
    path("admin/", admin.site.urls),
    # 进入默认站点，即进入网页后默认打开 smrWeb 应用
    path("", include("smrWeb.urls")),  # 指向 smrWeb/urls.py
]
