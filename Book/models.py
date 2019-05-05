from django.db import models
import datetime
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20, unique=True)
    pwd = models.CharField(max_length=20)
    college = models.CharField(max_length=20)
    stu_id = models.IntegerField()
    email = models.EmailField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    pub_date = models.DateField(auto_now_add=True)
    exist = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Borrow(models.Model):
    user = models.ForeignKey(to=User, on_delete=None)
    book = models.ForeignKey(to=Book, on_delete=None)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(default=datetime.date.today()+datetime.timedelta(days=30))


class HotPic(models.Model):
    name = models.CharField(max_length=50)
    index = models.SmallIntegerField(unique=True)
    path = models.ImageField(upload_to='Book')

    def __str__(self):
        return self.name


class UserImg(models.Model):
    path = models.ImageField(upload_to='UserImg')
