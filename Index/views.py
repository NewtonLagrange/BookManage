import io
import random
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, redirect, reverse
from Book import models
from hashlib import sha1
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings

# Create your views here.


def login(request):
    """ 登陆 """
    if request.session.get('username'):
        return redirect(reverse('Book:book'))

    if request.method == 'GET':
        return render(request, 'Index/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        verify_code_ = request.POST.get('verify_code')
        pwd = request.POST.get('pwd').encode('utf8')
        s = sha1()
        s.update(pwd)
        pwd = s.hexdigest()
        user = models.User.objects.filter(name=username, pwd=pwd).first()

        if user and user.is_active and verify_code_.lower() == request.session.get('verify_code').lower():
            request.session['username'] = username
            return redirect(reverse('Book:book'))
        else:
            return render(request, 'Index/login.html', {'failed': True})


def register(request):
    """ 注册 """
    if request.method == 'GET':
        return render(request, 'Index/register.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd').encode('utf8')
        college = request.POST.get('college')
        stu_id = request.POST.get('stu_id')
        email = request.POST.get('email')
        # 加密密码
        s = sha1()
        s.update(pwd)
        pwd = s.hexdigest()
        models.User.objects.create(name=username, pwd=pwd, college=college, stu_id=stu_id, email=email)
        # 加密连接
        serializer = Serializer(settings.SECRET_KEY, 60)
        username = serializer.dumps({'username': username}).decode('utf8')
        mail_content = '<a href="http://127.0.0.1:8000/verify/?username=%s">点击激活账户</a>' % username
        msg = EmailMultiAlternatives("点击链接验证你的账号", mail_content, 'niu_haiyang@qq.com', ['903095546@qq.com'])
        msg.content_subtype = 'html'
        msg.attach_file("./manage.py", "text/*")
        msg.send()
        return HttpResponse('请登录 <%s> 验证你的账号' % (email,))


def verify(request):
    username = request.GET.get('username')
    print(username)
    serializer = Serializer(settings.SECRET_KEY, 60)
    try:
        username = serializer.loads(username)['username']
    except SignatureExpired as e:
        print(e)
        return HttpResponse('链接过期了')

    user = models.User.objects.get(name=username)
    user.is_active = True
    user.save()
    return redirect(to=reverse('Index:login'))


def logout(request):
    request.session.clear()
    return redirect(reverse('Index:login'))


def verify_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100),
               random.randrange(20, 100),
               random.randrange(20, 100))
    width = 100
    height = 30
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
    fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
    draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('SCRIPTBL.TTF', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    request.session['verify_code'] = rand_str
    f = io.BytesIO()
    im.save(f, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    print(request.session.get('verify_code'))
    return HttpResponse(f.getvalue(), 'image/png')

