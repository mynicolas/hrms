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
                        'dogNP': 'checked'
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
                    'dogNP': ''
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
                    'dogNP': 'checked'
                }

            aUser['username'] = thisUsername
            aUser['query'] = query
            aUser['modify'] = modify
            allUsers.append(aUser)

        return render_to_response('allUsers.html', {'allUsers': allUsers})
    else:
        return HttpResponse('404 not found')


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
        if not thisUser:
            return HttpResponse('failed')
        else:
            thisUser = User.objects.get(username=username)
            try:
                thisPerm = thisUser.perm_set
                thisPerm.query = newQuery
                thisPerm.modify = newModify
                thisUser.save()
            except:
                thisUser.perm_set.create(query=newQuery, modify=newModify)
                thisUser.save()
            return HttpResponse('successful')
    else:
        return HttpResponse('404 not found')
