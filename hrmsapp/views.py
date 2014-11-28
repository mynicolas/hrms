#!/usr/bin/env python
#-*- coding: utf-8 -*-
from xml.dom import minidom
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from models import *


@login_required
@csrf_exempt
def renderVms(request):
    if request.method == "POST":
        if request.user.username == u'admin':
            vms = getVms()
        else:
            vms = getVms(user=request.user)

        ins = []
        for i in vms:
            vm = Vm(i)
            dogOs = vm.dogSn
            ipOs = vm.ip
            aIn = {}
            aIn['name'] = vm.instanceName
            aIn['vcpus'] = vm.vcpus
            aIn['mem'] = vm.mem
            aIn['disk'] = vm.dataDisk
            aIn['mac'] = vm.mac
            aIn['start'] = vm.startTime
            aIn['end'] = vm.useInterval
            aIn['company'] = vm.company
            aIn['bandwidth'] = vm.bandwidth
            aIn['nodes'] = vm.nodehost   # list
            ips = [ip for ip in ipOs]
            aIn['ips'] = ips            # list
            dogNP = ['%s:%s' % (i, dogOs[i]) for i in dogOs]
            aIn['dogNP'] = dogNP        # list
            ins.append(aIn)
        return render_to_response('all.html', {'all': ins})
        # return HttpResponse(ins)


@login_required
@csrf_exempt
def addHost(request):
    """
    添加实例
    参数中带有实例的详细信息
    """
    if request.method == "POST":
        vmName = request.POST.get('vmname', '')
        newVm = Vm(vmName)
        try:
            newVm.update(
                thisUser=request.user,
                vmName=vmName,
                vcpus=request.POST.get('vcpus', ''),
                mem=request.POST.get('mem', ''),
                dataDisk=request.POST.get('datadisk', ''),
                NodeHost=request.POST.get('nodehost', ''),
                startTime=request.POST.get('starttime', ''),
                useInterval=request.POST.get('endtime', ''),
                bandwidth=request.POST.get('bandwidth', ''),
                company=request.POST.get('company', ''),
                dogSn=request.POST.get('dogsn', ''),
                dogPort=request.POST.get('dogport', ''),
                ip=request.POST.get('ip', ''),
                mac=request.POST.get('mac', '')
            )
            return HttpResponse('successful')
        except:
            return HttpResponse('failed')


# @login_required
# @csrf_exempt
# def renderVms(request):
#     """
#     根据用户权限渲染实例项目
#     """
#     if request.method != "POST":
#         return 0
#     user = request.user
#     if user == u'root':
#         vms = getVms()
#     else:
#         vms = getVms(user=user)

#     sendContent = minidom.parseString("<xml></xml>")
#     root = sendContent.documentElement
#     for i in vms:
#         vm = Vm(i)
#         dogs = vm.dogSn
#         ips = vm.ip
#         vmXml = "\
#             <aHost>\
#                 <name>%s</name>\
#                 <core>%s</core>\
#                 <mem>%s</mem>\
#                 <disk>%s</disk>\
#                 <mac>%s</mac>\
#                 <start>%s</start>\
#                 <end>%s</end>\
#                 <company>%s</company>\
#                 <dogNP></dogNP>\
#                 <bandwidth>%s</bandwidth>\
#                 <node>%s</node>\
#                 <ips></ips>\
#             </aHost>\
#         " % (
#             vm.instanceName,
#             vm.vcpus,
#             vm.mem,
#             vm.dataDisk,
#             vm.mac,
#             vm.startTime,
#             vm.useInterval,
#             vm.company,
#             vm.bandwidth,
#             vm.nodeHost,
#             )
#         aVm = minidom.parseString(vmXml).documentElement
#         dogNP = aVm.getElementsByTagName('dogNp')
#         for p in dogs:
#             dogNPXml = "<dogN dogP='%s'>%s</dogN>" % (p, dogs[p])
#             dogNP.appendChild(minidom.parseString(dogNPXml).documentElement)
#         ipN = aVm.getElementsByTagName('ips')
#         for ip in ips:
#             ipXml = "<ip>%s</ip>" % ip
#             ipN.appendChild(minidom.parseString(ipXml).documentElement)

#         root.appendChild(aVm)
#     return HttpResponse(sendContent.toxml())


# @login_required
# @csrf_exempt
# def addIp(request):
#     """
#     添加IP
#     参数中带有需要添加的ip信息
#     """
#     if request.method == "POST":
#         try:
#             addIps(request.POST.get('ips', ''))
#             return HttpResponse('successful')
#         except:
#             return HttpResponse('failed')


# @login_required
# @csrf_exempt
# def addNode(request):
#     """
#     添加节点
#     参数中带有需要添加的节点信息
#     """
#     if request.method == "POST":
#         try:
#             addNodes(request.POST.get('nodes', ''))
#             return HttpResponse('successful')
#         except:
#             return HttpResponse('failed')


# @login_required
# @csrf_exempt
# def renderIpNode(request):
#     """
#     获取并返回ip池中的所有ip
#     param: request.POST['item']
#         item: ip || node
#     """
#     item = request.POST.get('item', '')
#     if item == u'ip':
#         ips = getIps()
#         return HttpResponse(ips)
#     elif item == u'node':
#         nodes = getNodes()
#         return HttpResponse(nodes)
