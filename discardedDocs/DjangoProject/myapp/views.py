# templates/views.py
from pyexpat.errors import messages

from django.http import HttpResponse
from .models import Book

from django.shortcuts import render, redirect, get_object_or_404


def home(request):
    return render(request, 'templates/home.html')


# 渲染login.html
def login_view(request):
    return render(request, 'templates/login.html')


# 检查登录状态
def check_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == '123456':
            # 登录成功后重定向到主页或其他页面
            return redirect('home')
        else:
            # 登录失败后重新显示登录页面，并提示错误
            messages.error(request, '登录失败')
            return redirect('login')
    else:
        return HttpResponse('无效的请求方式', status=405)


def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_date = request.POST.get('publication_date')
        book = Book(title=title, author=author, publication_date=publication_date)
        book.save()
        messages.success(request, '书籍添加成功！')
        return redirect('list_books')
    return render(request, 'templates/add_book.html')


def list_books(request):
    books = Book.objects.all()
    return render(request, 'templates/list_books.html', {'books': books})


def update_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_date = request.POST.get('publication_date')
        book.save()
        messages.success(request, '书籍更新成功！')
        return redirect('list_books')
    return render(request, 'templates/update_book.html', {'book': book})


def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, '书籍删除成功！')
        return redirect('list_books')
    return render(request, 'templates/delete_book.html', {'book': book})
