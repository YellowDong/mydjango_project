#coding=utf-8
from django.shortcuts import render, redirect
from .models import UserInfo
from hashlib import sha1
from django.http import HttpResponseRedirect


def register(request):
    return render(request, 'register_user/register.html')


def register_handle(request):
    #接收用户输入
    post = request.POST
    username = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')
    #判断两次密码输入是否一至
    if pwd != cpwd:
        return redirect('/register/')
    #对密码加密
    s = sha1()
    s.update(cpwd.encode('utf-8'))
    s1 = s.hexdigest()
    #创建对象
    user = UserInfo()
    user.username = username
    user.password = s1
    user.email = email
    user.save()
    return redirect('/register/login/')


def login(request):
    username = request.COOKIES.get('username', '')
    contex = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'username': username}
    return render(request, 'register_user/login.html', contex)


def login_handle(request):
    post = request.POST
    username = post.get('username')
    pwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(username=username)
    if len(users) == 1:
        s = sha1()
        s.update(pwd.encode('utf-8'))
        if s.hexdigest() == users[0].password:
            red = HttpResponseRedirect('/register/info')
            if jizhu != 0:
                red.set_cookie('username', username)
            else:
                red.set_cookie('username', username, max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = username
            return red
        else:
            contex = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'username': username, 'pwd': pwd}
            return render(request, 'register_user/login.html', contex)
    else:
        contex = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'username': username, 'pwd': pwd}
        return render(request, 'register_user/login.html', contex)


def info(request):
    username = request.COOKIES.get('username')
    contex = {'username': username}
    return render(request, 'register_user/user_center_info.html', contex)

