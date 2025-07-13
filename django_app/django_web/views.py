# django_web/views.py
# 函数声明
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Musician
from django.db import connection
from .models import Album


# 加载主页
def home_page(request):
    return render(request, 'web/home_page.html')


# 加载登录页
def log_in(request):
    return render(request, 'web/log_in.html')


# 登录检查
def log_check(request):
    # 获取用户名和密码参数
    uname = request.GET.get('uname', '')
    pwd = request.GET.get('pwd', '')
    # 判断用户名和密码是否正确
    if uname == 'JacksonHe04@outlook.com' and pwd == '1234':
        return render(request, 'web/home_page.html')
    else:
        return render(request, 'django_web/log_in.html')


# 加载音乐专辑
def albums_page(request):
    return render(request, 'web/albums_page.html')


# 加载发现音乐
def search_music(request):
    return render(request, 'web/search_music.html')


# 加载音乐人
def musicians_page(request):
    return render(request, 'web/musicians_page.html')


# 加载帮助
def help_page(request):
    return render(request, 'web/help_page.html')


# 加载关于
def about_page(request):
    return render(request, 'web/about_page.html')


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


# 在搜索框搜索音乐人名称
def musician_result(request):
    query = request.GET.get('query')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Musician WHERE name LIKE %s", ["%" + query + "%"])
        musician = dictfetchone(cursor)

    if not musician:
        return render(request, 'web/musicianResult.html', {'error_message': '音乐家未找到'})

    # 查询与该音乐家相关的所有专辑信息
    if musician:
        # 获取音乐家的三张专辑的 ID（album1, album2, album3）
        album1_id = musician['album1']
        album2_id = musician['album2']
        album3_id = musician['album3']

        # 确保 album_id 不为 None，查询专辑详细信息
        albums = []
        if album1_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Album WHERE id = %s", [album1_id])
                album1 = dictfetchone(cursor)
                if album1:
                    albums.append(album1)

        if album2_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Album WHERE id = %s", [album2_id])
                album2 = dictfetchone(cursor)
                if album2:
                    albums.append(album2)

        if album3_id:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Album WHERE id = %s", [album3_id])
                album3 = dictfetchone(cursor)
                if album3:
                    albums.append(album3)

    return render(request, 'web/musician_result.html', {'musician': musician, 'albums': albums})


# 从音乐人页面进入专辑
def album_result(request, album_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Album WHERE id = %s", [album_id])
        album = dictfetchone(cursor)

    if not album:
        return render(request, 'web/albumResult.html', {'error_message': '专辑未找到'})

    # 获取该专辑的音乐人信息
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.* FROM Musician m
            JOIN Musician_album ma ON m.id = ma.musician_id
            WHERE ma.album_id = %s
        """, [album_id])
        musician = dictfetchone(cursor)

    # 获取该音乐人的其他专辑（排除当前专辑）
    other_albums = []
    if musician:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.* FROM Album a
                JOIN Musician_album ma ON a.id = ma.album_id
                WHERE ma.musician_id = %s AND a.id != %s
            """, [musician['id'], album_id])
            other_albums = dictfetchall(cursor)

    # 渲染模板并传递数据
    return render(request, 'web/album_result.html', {
        'album': album,
        'other_albums': other_albums,
    })


# 在搜索框搜索专辑名称
def album_result_search(request):
    query = request.GET.get('query')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Album WHERE title LIKE %s", ["%" + query + "%"])
        album = dictfetchone(cursor)

    if not album:
        return render(request, 'web/albumResult.html', {'error_message': '专辑未找到'})

    # 获取该专辑的音乐人信息
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT m.* FROM Musician m
                JOIN Musician_album ma ON m.id = ma.musician_id
                WHERE ma.album_id = %s
            """, [album['id']])
        musician = dictfetchone(cursor)

    # 获取该音乐人的其他专辑（排除当前专辑）
    other_albums = []
    if musician:
        with connection.cursor() as cursor:
            cursor.execute("""
                    SELECT a.* FROM Album a
                    JOIN Musician_album ma ON a.id = ma.album_id
                    WHERE ma.musician_id = %s AND a.id != %s
                """, [musician['id'], album['id']])
            other_albums = dictfetchall(cursor)

    # 渲染模板并传递数据
    return render(request, 'web/album_result.html', {
        'album': album,
        'musician': musician,
        'other_albums': other_albums,  # 推荐专辑
    })
