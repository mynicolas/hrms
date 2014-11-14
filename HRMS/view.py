#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from getdata import *
from HRMSApp.models import *

@login_required
def redirectLogin(request):
    """
    如果没有登陆，重定向到登陆页面，如果已登陆，则进入主页
    """
    return HttpResponseRedirect('/index/')

def renderLogin(request):
    """
    渲染登陆视图
    """
    return render_to_response('login.html')

@login_required
def renderIndex(request):
    """
    如果没有登陆，重定向到登陆页面，如果已经登陆则渲染主页视图
    """
    return render_to_response('index.html', {'username': request.user.username})

@csrf_exempt
def login(request):
    """
    获取post到服务器的用户名密码，如果用户名和密码正确则登陆并进入主页，如果不正确则返回'error'
    """
    if request.method == 'POST':
        username = smart_str(request.POST['username'])
        password = smart_str(request.POST['password'])
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            return HttpResponse('error')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = smart_str(request.POST['username'])
        password = smart_str(request.POST['password'])
        company = smart_str(request.POST['company'])
        email = smart_str(request.POST['email'])
        weixin = smart_str(request.POST['weixin'])
        phone = smart_str(request.POST['phone'])
        question = smart_str(request.POST['question'])
        answer = smart_str(request.POST['answer'])
        try:
            User.objects.get(username = username)
            return HttpResponse('username existed')
        except:
            try:
                thisCompany = Company.objects.get(companyName = company)
            except:
                thisCompany = Company.objects.create(companyName = company)

            thisUser = thisCompany.profile_set
            thisUser.create(weixin = weixin, phone = phone, question = question, answer = answer, 
                user = User.objects.create_user(username = username, password = password, email = email))
            thisCompany.save()
            thisUser = User.objects.get(username = username)
            thisUser.is_stuff = False
            thisUser.is_active = False
            thisUser.is_superuser = False
            thisUser.save()
            return HttpResponse('register successful')
    else:
        return HttpResponse('404 not found')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

@csrf_exempt
@login_required
def renderAllUsers(request):
    """
    获取所有用户及相关信息
    :return: <xml>
                <user>
                    <username>username</username>
                    <password>password</password>
                    <email>email</email>
                    <datejoined>date_joined</datejoined>
                    <lastlogin>last_login</lastlogin>
                    <isactive>is_active</isactive>
                    <isstuff>is_stuff</isstuff>
                    <weixin>weixinid</weixin>
                    <phone>phone</phone>
                    <question>question</question>
                    <answer>answer</answer>
                </user>
                ... ...
            </xml>
    """
    if request.method == "POST":
        if smart_str(request.POST['users']) == "allusers":
            users = getAllUsers()
            sendContent = "<xml>"
            for aUser in users:
                sendContent += "<user>"
                sendContent += "<username>%s</username>" % aUser['username'].encode('utf-8')
                sendContent += "<password>%s</password>" % aUser['password'].encode('utf-8')
                sendContent += "<email>%s</email>" % aUser['email'].encode('utf-8')
                sendContent += "<company>%s</company>" % aUser['companyname'].encode('utf-8')
                sendContent += "<datejoined>%s</datejoined>" % aUser['date_joined'].encode('utf-8')
                sendContent += "<lastlogin>%s</lastlogin>" % aUser['last_login'].encode('utf-8')
                sendContent += "<isactive>%s</isactive>" % aUser['is_active'].encode('utf-8')
                sendContent += "<isstaff>%s</isstaff>" % aUser['is_staff'].encode('utf-8')
                sendContent += "<weixin>%s</weixin>" % aUser['weixin'].encode('utf-8')
                sendContent += "<phone>%s</phone>" % aUser['phone'].encode('utf-8')
                sendContent += "<question>%s</question>" % aUser['question'].encode('utf-8')
                sendContent += "<answer>%s</answer>" % aUser['answer'].encode('utf-8')
                sendContent += "</user>"
            sendContent += "</xml>"
    else:
        sendContent = "error"
    return HttpResponse(sendContent)


@csrf_exempt
@login_required
def modifyUserItem(request):
    if request.method == "POST":
        username = smart_str(request.POST['username'])
        userItem = smart_str(request.POST['useritem'])
        if userItem == 'password':
            isModify = setPassword(username)
        elif userItem == 'isactive' or userItem == 'isstaff':
            value = smart_str(request.POST['value'])
            isModify = modifyUserStatus(username, userItem, value)

        if isModify:
            sendContent = "successful"
        else:
            sendContent = "failed"
    else:
        sendContent = "404 not found"
    return HttpResponse(sendContent)

@csrf_exempt
@login_required
def test(request):
    return HttpResponse(type(request.user.username))