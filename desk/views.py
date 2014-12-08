#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required
def renderDesk(request):
    """
    渲染桌面
    """
    isAdmin = request.user.is_superuser
    return render_to_response('index.html', {'admin': isAdmin})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')
