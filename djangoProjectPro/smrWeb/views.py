# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Musician
from django.db import connection


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


# albums_page
def albums_page(request):
    return render(request, 'smrWeb/albums_page.html')


# search_music
def search_music(request):
    return render(request, 'smrWeb/search_music.html')


# musicians_page
def musicians_page(request):
    return render(request, 'smrWeb/musicians_page.html')


# service_page
def help_page(request):
    return render(request, 'smrWeb/help_page.html')


# more_page
def about_page(request):
    return render(request, 'smrWeb/about_page.html')


# musicain_result
# def musician_result(request):
#     return render(request, 'smrWeb/musician_result.html')


# album_result
def album_result(request):
    return render(request, 'smrWeb/album_result.html')


def dictfetchone(cursor):
    """将查询结果转换为字典"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    return dict(zip(columns, row))


def dictfetchall(cursor):
    """将查询结果转换为字典列表"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def musician_result(request):
    query = request.GET.get('query')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Musician WHERE name = %s", [query])
        musician = dictfetchone(cursor)

    if not musician:
        return render(request, 'smrWeb/musicianResult.html', {'error_message': '音乐家未找到'})

    # 输出 musician 元组以确认数据格式
    print(f"Musician: {musician}")

    # 查询与该音乐家相关的所有专辑信息
    if musician:
        musician_id = musician['id']
        with connection.cursor() as cursor:
            cursor.execute("""
                   SELECT a.* 
                   FROM Album a 
                   JOIN Musician_Album ma ON a.id = ma.album_id 
                   WHERE ma.musician_id = %s
               """, [musician_id])
            albums = dictfetchall(cursor)
            # 输出 albums 字典列表以确认数据格式
        print(f"Albums: {albums}")
    else:
        albums = []

    print(f"Final musician: {musician}")
    print(f"Final albums: {albums}")

    return render(request, 'smrWeb/musician_result.html', {'musician': musician, 'albums': albums})
