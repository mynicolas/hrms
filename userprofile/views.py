#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
from models import *
from log.models import *


@csrf_exempt
@login_required
def renderAllUsers(request):
    if request.method == "POST":
        allUserOs = User.objects.all()
        allUsers = []
        for aUserO in allUserOs:
            aUser = {}
            thisUsername = aUserO.username
            try:
                thisUserPerm = aUserO.perm_set.all()[0]
                queryList = thisUserPerm.query.split(',')
                modifyList = thisUserPerm.modify.split(',')
                query = {}
                modify = {}
                if aUserO.is_superuser:
                    query = modify = {
                        'instanceName': 'checked',
                        'vcpus': 'checked',
                        'mem': 'checked',
                        'dataDisk': 'checked',
                        'startTime': 'checked',
                        'useInterval': 'checked',
                        'company': 'checked',
                        'bandwidth': 'checked',
                        'nodeHost': 'checked',
                        'macAddress': 'checked',
                        'ipAddress': 'checked',
                        'dogNP': 'checked',
                        'businessMan': 'checked'
                    }
                else:
                    for q in queryList:
                        query[q] = 'checked'
                    for m in modifyList:
                        modify[m] = 'checked'

                    if not query.get('instanceName', ''):
                        query['instanceName'] = ''
                    if not query.get('vcpus', ''):
                        query['vcpus'] = ''
                    if not query.get('mem', ''):
                        query['mem'] = ''
                    if not query.get('dataDisk', ''):
                        query['dataDisk'] = ''
                    if not query.get('startTime', ''):
                        query['startTime'] = ''
                    if not query.get('useInterval', ''):
                        query['useInterval'] = ''
                    if not query.get('company', ''):
                        query['company'] = ''
                    if not query.get('bandwidth', ''):
                        query['bandwidth'] = ''
                    if not query.get('nodeHost', ''):
                        query['nodeHost'] = ''
                    if not query.get('macAddress', ''):
                        query['macAddress'] = ''
                    if not query.get('ipAddress', ''):
                        query['ipAddress'] = ''
                    if not query.get('dogNP', ''):
                        query['dogNP'] = ''
                    if not query.get('businessMan', ''):
                        query['businessMan'] = ''

                    if not modify.get('instanceName', ''):
                        modify['instanceName'] = ''
                    if not modify.get('vcpus', ''):
                        modify['vcpus'] = ''
                    if not modify.get('mem', ''):
                        modify['mem'] = ''
                    if not modify.get('dataDisk', ''):
                        modify['dataDisk'] = ''
                    if not modify.get('startTime', ''):
                        modify['startTime'] = ''
                    if not modify.get('useInterval', ''):
                        modify['useInterval'] = ''
                    if not modify.get('company', ''):
                        modify['company'] = ''
                    if not modify.get('bandwidth', ''):
                        modify['bandwidth'] = ''
                    if not modify.get('nodeHost', ''):
                        modify['nodeHost'] = ''
                    if not modify.get('macAddress', ''):
                        modify['macAddress'] = ''
                    if not modify.get('ipAddress', ''):
                        modify['ipAddress'] = ''
                    if not modify.get('dogNP', ''):
                        modify['dogNP'] = ''
                    if not modify.get('businessMan', ''):
                        modify['businessMan'] = ''
            except:
                modify = {
                    'instanceName': '',
                    'vcpus': '',
                    'mem': '',
                    'dataDisk': '',
                    'startTime': '',
                    'useInterval': '',
                    'company': '',
                    'bandwidth': '',
                    'nodeHost': '',
                    'macAddress': '',
                    'ipAddress': '',
                    'dogNP': '',
                    'businessMan': ''
                }
                query = {
                    'instanceName': 'checked',
                    'vcpus': 'checked',
                    'mem': 'checked',
                    'dataDisk': 'checked',
                    'startTime': 'checked',
                    'useInterval': 'checked',
                    'company': 'checked',
                    'bandwidth': 'checked',
                    'nodeHost': '',
                    'macAddress': '',
                    'ipAddress': 'checked',
                    'dogNP': 'checked',
                    'businessMan': 'checked'
                }

            aUser['username'] = thisUsername
            aUser['query'] = query
            aUser['modify'] = modify
            allUsers.append(aUser)

        return render_to_response('allUsers.html', {'allUsers': allUsers})
    else:
        raise Http404


@csrf_exempt
@login_required
def changePerm(request):
    """
    修改用户的权限
    """
    if request.method == "POST":
        username = request.POST.get('username', '')
        oldQuery = request.POST.get('oldquery', '')
        newQuery = request.POST.get('newquery', '')
        oldModify = request.POST.get('oldmodify', '')
        newModify = request.POST.get('newmodify', '')
        if not username:
            return HttpResponse('failed')
        else:
            thisUser = User.objects.get(username=username)
            try:
                thisPerm = thisUser.perm_set.all()[0]
                thisPerm.query = newQuery
                thisPerm.modify = newModify
                thisPerm.save()
            except:
                try:
                    thisUser.perm_set.create(query=newQuery, modify=newModify)
                    thisUser.save()
                except:
                    return HttpResponse('failed')
            log = LogRequest(request.user)
            if not oldQuery == newQuery:
                log.save(
                    '(change %s query permission) %s --> %s' %
                    (username, oldQuery, newQuery)
                    )
            if not oldModify == newModify:
                log.save(
                    '(change %s modify permission) %s --> %s' %
                    (username, oldModify, newModify)
                    )
            return HttpResponse('successful')
    else:
        raise Http404


@csrf_exempt
@login_required
def changeSort(request):
    """
    改变该用户的实例排序
    """
    if request.method == "POST":
        vmSort = request.POST.get('vmsort', '')[1:-1]
        if vmSort:
            thisPerm = request.user.perm_set.all()
            if thisPerm:
                thisPerm[0].sort = vmSort
                thisPerm[0].save()
            else:
                newPerm = request.user.perm_set.create(
                    query=',vmName,vcpus,mem,dataDisk,startTime,useInterval,company,bandwidth,ipAddress,dogNP,',
                    modify=',',
                    sort=vmSort
                    )
                newPerm.save()
            return HttpResponse('successful')
        else:
            return HttpResponse('failed')
    else:
        raise Http404
