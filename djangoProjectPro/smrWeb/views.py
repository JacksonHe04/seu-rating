# views.py
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

# home_page
def home_page(request):
    """处理主页请求"""
    return render(request, 'smrWeb/home_page.html')


# log_in
def log_in(request):
    return render(request, 'smrWeb/log_in.html')


# log/check
def log_check(request):
    # 获取用户名和密码参数
    uname = request.GET.get('uname', '')
    pwd = request.GET.get('pwd', '')
    # 判断用户名和密码是否正确
    if uname == 'JacksonHe04@outlook.com' and pwd == '1234':
        return render(request, 'smrWeb/home_page.html')
    else:
        return render(request, 'smrWeb/log_in.html')


# album_page
def albums_page(request):
    return render(request, 'smrWeb/albums_page.html')


# search_music
def search_music(request):
    return render(request, 'smrWeb/search_music.html')


# musician_page
def musician_page(request):
    return render(request, 'smrWeb/musician_page.html')


# service_page
def help_page(request):
    return render(request, 'smrWeb/help_page.html')


# more_page
def about_page(request):
    return render(request, 'smrWeb/about_page.html')


# result1
def musician_result(request):
    return render(request, 'smrWeb/musician_result.html')
