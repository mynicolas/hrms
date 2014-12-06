#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str


def renderLogin(request):
    """
    渲染登陆视图
    """
    return render_to_response('login.html')


@csrf_exempt
def register(request):
    """
    注册新用户
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            try:
                newUser = User.objects.create_user(
                    username=username,
                    password=password
                )
                newUser.is_active = True
                if username == u'admin':
                    newUser.is_superuser = True
                    newUser.perm_set.create(query='all', modify='all')
                else:
                    newUser.is_superuser = False
                newUser.is_staff = True
                newUser.save()
                return HttpResponse('successful')
            except:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')


@csrf_exempt
def checkUser(request):
    """
    判断该用户名是否已被注册
    request: keys('username')
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        if username:
            try:
                User.objects.get(username=username)
                return HttpResponse('failed')
            except:
                return HttpResponse('successful')
        else:
            return HttpResponse('failed')


@csrf_exempt
def checkLogin(request):
    """
    检查用户名密码，如果该用户有登录权限，则重定向到主页
    request: keys('username', 'password')
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')

