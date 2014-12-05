#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import *


@csrf_exempt
@login_required
def renderLogs(request):
    """
    渲染用户的日志
    """
    log = LogRequest(request.user)
    sendContent = log.get()
    return render_to_response('allLogs.html', {'logs': sendContent})
