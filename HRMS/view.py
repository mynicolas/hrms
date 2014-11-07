#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str

def renderLogin(request):
    return render_to_response('login.html')

def renderIndex(request):
    return render_to_response('index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = smart_str(request.POST['username'])
        password = smart_str(request.POST['password'])
        return HttpResponse('/index/')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = smart_str(request.POST['username'])
        password = smart_str(request.POST['password'])
        email = smart_str(request.POST['email'])
        try:
            User.objects.get(username = username)
            return HttpResponse('username existed')
        except:
            newUser = User.objects.create_user(username = username, email = email, password = password)
            newUser.is_staff = True
            newUser.is_active = True
            newUser.save()
        return HttpResponse('register successful')
    else:
        return HttpResponse('404 not found')