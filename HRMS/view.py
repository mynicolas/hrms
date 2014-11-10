#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str

@login_required
def redirectLogin(request):
    return HttpResponseRedirect('/index/')

def renderLogin(request):
    return render_to_response('login.html')

@login_required
def renderIndex(request):
    return render_to_response('index.html')

# @csrf_exempt
@csrf_exempt
def login(request):
    if request.method == 'POST':
        return HttpResponse(smart_str(request.POST['password']))
        # username = smart_str(request.POST['username'])
        # password = smart_str(request.POST['password'])
        # user = auth.authenticate(username = username, password = password)
        # if user is not None and user.is_active:
        #     auth.login(request, user)
        #     return HttpResponseRedirect('/index/')
        # else:
        #     return HttpResponse('error')

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

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')