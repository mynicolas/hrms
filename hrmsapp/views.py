#!/usr/bin/env python
#-*- coding: utf-8 -*-
# from xml.dom import minidom
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
        vms = getVms()

        ins = []
        for i in vms:
            vm = Vm(i)
            dogOs = vm.dogSn    # dogObjects
            ipOs = vm.ip        # ipObjects
            macOs = vm.mac      # macObjects
            aIn = {}            # aInstance
            aIn['name'] = {
                'valu': vm.instanceName,
                'perm': 'enabled',
                'visi': True
            }
            aIn['vcpus'] = {
                'valu': vm.vcpus,
                'perm': 'enabled',
                'visi': True
            }
            aIn['mem'] = {
                'valu': vm.mem,
                'perm': 'enabled',
                'visi': True
            }
            aIn['disk'] = {
                'valu': vm.dataDisk,
                'perm': 'enabled',
                'visi': True
            }
            aIn['start'] = {
                'valu': vm.startTime,
                'perm': 'enabled',
                'visi': True
            }
            aIn['end'] = {
                'valu': vm.useInterval,
                'perm': 'enabled',
                'visi': True
            }
            aIn['company'] = {
                'valu': vm.company,
                'perm': 'enabled',
                'visi': True
            }
            aIn['bandwidth'] = {
                'valu': vm.bandwidth,
                'perm': 'enabled',
                'visi': True
            }
            aIn['node'] = {
                'valu': vm.nodeHost,
                'perm': 'enabled',
                'visi': True
            }
            aIn['macs'] = {
                'valu': [mac.macAddress for mac in macOs],
                'perm': 'enabled',
                'visi': True
            }           # list
            ips = [ip.ipAddress for ip in ipOs]
            aIn['ips'] = {
                'valu': ips,
                'perm': 'enabled',
                'visi': True
            }           # list
            dogNP = ['%s:%s' % (i, dogOs[i]) for i in dogOs]
            aIn['dogNP'] = {
                'valu': dogNP,
                'perm': 'enabled',
                'visi': True
            }           # list
            ins.append(aIn)
        return render_to_response('all.html', {'all': ins, 'header': ins[0]})


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
                owner=request.user.username,
                vcpus=request.POST.get('vcpus', ''),
                mem=request.POST.get('mem', ''),
                dataDisk=request.POST.get('datadisk', ''),
                nodeHost=request.POST.get('nodehost', ''),
                startTime=request.POST.get('starttime', ''),
                useInterval=request.POST.get('endtime', ''),
                bandwidth=request.POST.get('bandwidth', ''),
                company=request.POST.get('company', ''),
                mac=request.POST.get('mac', ''),
                dogSn=[
                    request.POST.get('dogsn', ''),
                    request.POST.get('dogport', '')
                ],
                ip=[
                    request.POST.get('ip', '')
                ]
            )
            return HttpResponse('successful')
        except:
            return HttpResponse('failed')


@csrf_exempt
@login_required
def renderNodes(request):
    """
    渲染所有nodes
    """
    if request.method == "POST":
        nodes = NodeHost.objects.all()
        allNodes = [i.node for i in nodes]
        return render_to_response('nodes.html', {'nodes': allNodes})


@csrf_exempt
@login_required
def renderDogPorts(request):
    """
    渲染所有未被使用的dogports
    """
    if request.method == "POST":
        thisNodeName = smart_str(request.POST.get('node', ''))
        try:
            thisNode = NodeHost.objects.get(node=thisNodeName)
        except:
            return HttpResponse('failed')
        dogPorts = thisNode.usbport_set.all()
        sendContent = []
        for dogPort in dogPorts:
            if not dogPort.instance:
                sendContent.append(dogPort.port)
        return render_to_response('ports.html', {'ports': sendContent})
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def renderIps(request):
    """
    渲染所有未被使用的ip
    """
    if request.method == "POST":
        ips = Ip.objects.all()
        sendContent = []
        for ip in ips:
            if not ip.instance:
                sendContent.append(ip.ipAddress)
        return render_to_response('ips.html', {'ips': sendContent})
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def renderMacs(request):
    """
    渲染所有未被使用的ip
    """
    if request.method == "POST":
        macs = Mac.objects.all()
        sendContent = []
        for mac in macs:
            if not mac.instance:
                sendContent.append(mac.macAddress)
        return render_to_response('macs.html', {'macs': sendContent})
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def addNode(request):
    """
    添加nodes
    """
    if request.method == "POST":
        node = request.POST.get('newNode', '')
        if node:
            try:
                NodeHost.objects.get(node=node)
                return HttpResponse('failed')
            except:
                newNode = NodeHost.objects.create(node=node)
                newNode.save()
                return HttpResponse('successful')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def addIp(request):
    """
    添加IP
    """
    if request.method == "POST":
        ip = request.POST.get('newIp', '')
        if ip:
            try:
                Ip.objects.get(ipAddress=ip)
                return HttpResponse('failed')
            except:
                newIp = Ip.objects.create(ipAddress=ip)
                newIp.save()
                return HttpResponse('successful')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def addDogPort(request):
    """
    添加狗
    """
    if request.method == "POST":
        newDogPort = request.POST.get('dogPort', '')
        thisNode = request.POST.get('node', '')
        if newDogPort and thisNode:
            try:
                UsbPort.objects.get(port=newDogPort)
                return HttpResponse('faild')
            except:
                try:
                    newPort = NodeHost.objects.get(node=thisNode)
                except:
                    return HttpResponse('faild')
                else:
                    newPort.usbport_set.create(port=newDogPort)
                    newPort.save()
                    return HttpResponse('successful')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def addMac(request):
    """
    添加mac
    """
    if request.method == "POST":
        thisMac = request.POST.get('newMac', '')
        if thisMac:
            try:
                Mac.objects.get(macAddress=thisMac)
                return HttpResponse('failed')
            except:
                newMac = Mac.objects.create(macAddress=thisMac)
                newMac.save()
                return HttpResponse('successful')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def modify(request):
    """
    修改实例数据
    """
    if request.method == "POST":
        thisHost = smart_str(request.POST.get('host', ''))
        thisItem = smart_str(request.POST.get('item', ''))
        # oldValue = smart_str(request.POST.get('oldvalue', ''))
        newValue = smart_str(request.POST.get('newvalue', ''))

        thisVm = Vm(thisHost)
        if not thisVm.existed:
            return HttpResponse('failed')
        else:
            try:
                if thisItem == "hostName":
                    thisVm.update(vmName=newValue)
                elif thisItem == "vcpus":
                    thisVm.update(vcpus=newValue)
                elif thisItem == "mem":
                    thisVm.update(mem=newValue)
                elif thisItem == "disk":
                    thisVm.update(dataDisk=newValue)
                elif thisItem == "start":
                    thisVm.update(startTime=newValue)
                elif thisItem == "end":
                    thisVm.update(useInterval=newValue)
                elif thisItem == "company":
                    thisVm.update(company=newValue)
                elif thisItem == "bandwidth":
                    thisVm.update(bandwidth=newValue)
                elif thisItem == "node":
                    thisVm.update(nodeHost=newValue)

                return HttpResponse('successful')
            except:
                return HttpResponse('failed')
    else:
        return HttpResponse('404 not found')


@csrf_exempt
@login_required
def renderAddMacs(request):
    """
    渲染添加mac的对话框
    """
    if request.method == "POST":
        if request.POST.get('dialog', ''):
            vm = Vm(smart_str(request.POST.get('host')))
            macs = [macOs.macAddress for macOs in vm.mac]
            allMacOs = Mac.objects.all()
            freeMacs = [
                aMacOs.macAddress for aMacOs in allMacOs if not aMacOs.instance
            ]
            return HttpResponse("%s/%s" % (macs, freeMacs))
        else:
            return HttpResponse('failed')


@csrf_exempt
@login_required
def addMacs(request):
    """
    为某个实例添加或删除mac
    """
    if request.method == "POST":
        return HttpResponse('successful')

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
