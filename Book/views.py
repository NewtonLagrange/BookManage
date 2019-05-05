from django.shortcuts import render, reverse, redirect
from .models import Book, Borrow, User, HotPic, UserImg
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

# Create your views here.


@cache_page(60*5)
def book(request):
    books = Book.objects.all()
    username = request.session['username']
    hot_pics = HotPic.objects.all()
    print(hot_pics)
    return render(request, 'Book/books.html', {'books': books, 'username': username, 'hot_pics': hot_pics})


def borrow(request, book_id):
    book_ = Book.objects.get(pk=book_id)
    user = User.objects.get(name=request.session['username'])
    Borrow.objects.create(user=user, book=book_)
    book_.exist = False
    book_.save()
    return redirect(reverse('Book:book'))


def user_info(request):
    user = User.objects.get(name=request.session['username'])
    return render(request, 'Book/user_info.html', {'user': user, 'username': user.name})


def borrow_record(request):
    user = User.objects.get(name=request.session['username'])
    borrows = user.borrow_set.all()
    return render(request, 'Book/borrow_record.html', {'borrows': borrows, 'username': user.name})


def search(request):
    if request.method == 'GET':
        return render(request, 'Book/search.html', {'username': request.session['username']})

    elif request.method == 'POST':
        book_info = request.POST.get('book_info')
        books = Book.objects.filter(Q(name__contains=book_info) | Q(author__contains=book_info))
        return render(request, 'Book/search.html', {'books': books, 'username': request.session['username']})


def upload(request):
    if request.method == 'GET':
        return render(request, 'Book/upload.html')

    elif request.method == 'POST':
        img = request.FILES['img']
        user_img = UserImg(path=img)
        user_img.save()
        return redirect(to=reverse('Book:book'))


def ajax(request):
    if request.method == 'POST':
        return HttpResponse('成功点击')


def test(request):
    return render(request, 'Book/test.html')

