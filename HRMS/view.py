#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def renderLogin(request):
    return render_to_response('login.html')

def renderIndex(request):
    return render_to_response('index.html')

def login(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/index')