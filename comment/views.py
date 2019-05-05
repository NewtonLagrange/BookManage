from django.shortcuts import render, redirect, reverse
from Book.models import User
from . import models


# Create your views here.
def comment(request):
    if request.method == 'POST':
        user = User.objects.get(name=request.session['username'])
        comment_ = request.POST.get('comment')
        comment_ = models.Comment(content=comment_, user=user)
        comment_.save()
        return redirect(to=reverse('Book:book'))

    elif request.method == 'GET':
        return render(request, 'comment/comment.html', {'username': request.session['username']})
