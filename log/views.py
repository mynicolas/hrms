#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import Http404
from models import *
import datetime
from hrmsapp.models import *


@csrf_exempt
@login_required
def renderLogs(request):
    """
    渲染用户的日志
    """
    log = LogRequest(request.user)
    logs = log.get()
    return render_to_response('allLogs.html', {'logs': logs})


@csrf_exempt
@login_required
def renderHosts(request):
    """
    为log条件查询渲染所有该用户的实例名
    """
    if request.method == "POST":
        thisUser = request.user
        if thisUser.is_superuser:
            hostNames = getVms()
        else:
            hostNames = getVms(user=thisUser)
        return render_to_response(
            'allHostNames.html',
            {'hostNames': hostNames}
            )
    else:
        raise Http404


@csrf_exempt
@login_required
def conditionLog(request):
    if request.method == "POST":
        hostName = request.POST.get('hostname', '')
        startTime = request.POST.get('starttime', None)
        endTime = request.POST.get('endtime', None)

        log = LogRequest(request.user)
        if hostName and not startTime and not endTime:
            logs = log.get(host=hostName)
        elif not hostName and startTime and endTime:
            logs = log.get(
                startTime=string2Date(startTime),
                endTime=string2Date(endTime) + datetime.timedelta(1)
                )
        elif hostName and startTime and endTime:
            logs = log.get(
                host=hostName,
                startTime=string2Date(startTime),
                endTime=string2Date(endTime) + datetime.timedelta(1)
                )
        else:
            return HttpResponse('query error')

        return render_to_response('allLogs.html', {'logs': logs})
    else:
        raise Http404
