#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str


@csrf_exempt
@login_required
def renderDesk(request):
	"""
	渲染桌面
	"""
	return render_to_response('index.html')


@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login/')
