#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
def checkLogin(request):
	"""
	检查用户名密码，如果该用户有登录权限，则重定向到主页
	request: keys('username', 'password')
	"""
	pass
