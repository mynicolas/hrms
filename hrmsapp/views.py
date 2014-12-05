#!/usr/bin/env python
#-*- coding: utf-8 -*-
# from xml.dom import minidom
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import *


@login_required
@csrf_exempt
def renderVms(request):
    if request.method == "POST":
        thisUser = request.user
        if thisUser.username == u'admin':
            vms = getVms()
        else:
            vms = getVms(user=request.user)
        vms = getVms()

        try:
            permission = thisUser.perm_set.all()[0]
            queryList = permission.query.split(',')
            modifyList = permission.modify.split(',')
            query = {}
            modify = {}
            if thisUser.is_superuser:
                query = {
                    'instanceName': True,
                    'vcpus': True,
                    'mem': True,
                    'dataDisk': True,
                    'startTime': True,
                    'useInterval': True,
                    'company': True,
                    'bandwidth': True,
                    'nodeHost': True,
                    'macAddress': True,
                    'ipAddress': True,
                    'dogNP': True
                }
                modify = {
                    'instanceName': 'enabled',
                    'vcpus': 'enabled',
                    'mem': 'enabled',
                    'dataDisk': 'enabled',
                    'startTime': 'enabled',
                    'useInterval': 'enabled',
                    'company': 'enabled',
                    'bandwidth': 'enabled',
                    'nodeHost': 'enabled',
                    'macAddress': 'enabled',
                    'ipAddress': 'enabled',
                    'dogNP': 'enabled'
                }
            else:
                for q in queryList:
                    query[q] = True
                for m in modifyList:
                    modify[m] = 'enabled'

        except:
            modify = {
                'instanceName': 'disabled',
                'vcpus': 'disabled',
                'mem': 'disabled',
                'dataDisk': 'disabled',
                'startTime': 'disabled',
                'useInterval': 'disabled',
                'company': 'disabled',
                'bandwidth': 'disabled',
                'nodeHost': 'disabled',
                'macAddress': 'disabled',
                'ipAddress': 'disabled',
                'dogNP': 'disabled'
            }
            query = {
                'instanceName': True,
                'vcpus': True,
                'mem': True,
                'dataDisk': True,
                'startTime': True,
                'useInterval': True,
                'company': True,
                'bandwidth': True,
                'nodeHost': False,
                'macAddress': False,
                'ipAddress': True,
                'dogNP': True
            }

        ins = []
        for i in vms:
            vm = Vm(i)
            dogOs = vm.dogSn    # dogObjects
            ipOs = vm.ip        # ipObjects
            macOs = vm.mac      # macObjects
            aIn = {}            # aInstance
            aIn['name'] = {
                'value': vm.instanceName,
                'modify': modify.get('instanceName', 'disabled'),
                'query': query.get('instanceName', False)
            }
            aIn['vcpus'] = {
                'value': vm.vcpus,
                'modify': modify.get('vcpus', 'disabled'),
                'query': query.get('vcpus', False)
            }
            aIn['mem'] = {
                'value': vm.mem,
                'modify': modify.get('mem', 'disabled'),
                'query': query.get('mem', False)
            }
            aIn['disk'] = {
                'value': vm.dataDisk,
                'modify': modify.get('dataDisk', 'disabled'),
                'query': query.get('dataDisk', False)
            }
            aIn['start'] = {
                'value': vm.startTime,
                'modify': modify.get('startTime', 'disabled'),
                'query': modify.get('startTime', False)
            }
            aIn['end'] = {
                'value': vm.useInterval,
                'modify': modify.get('useInterval', 'disabled'),
                'query': query.get('useInterval', False)
            }
            aIn['company'] = {
                'value': vm.company,
                'modify': modify.get('company', 'disabled'),
                'query': query.get('company', False)
            }
            aIn['bandwidth'] = {
                'value': vm.bandwidth,
                'modify': modify.get('bandwidth', 'disabled'),
                'query': query.get('bandwidth', False)
            }
            aIn['node'] = {
                'value': vm.nodeHost,
                'modify': modify.get('nodeHost', 'disabled'),
                'query': query.get('nodeHost', False)
            }
            aIn['macs'] = {
                'value': [mac.macAddress for mac in macOs],
                'modify': modify.get('macAddress', 'disabled'),
                'query': query.get('macAddress', False)
            }           # list
            ips = [ip.ipAddress for ip in ipOs]
            aIn['ips'] = {
                'value': ips,
                'modify': modify.get('ipAddress', 'disabled'),
                'query': query.get('ipAddress', False)
            }           # list
            dogNP = ['%s:%s' % (i, dogOs[i]) for i in dogOs]
            aIn['dogNP'] = {
                'value': dogNP,
                'modify': modify.get('dogNP', 'disabled'),
                'query': query.get('dogNP', False)
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
        if newVm.existed:
            return HttpResponse('failed')
        try:
            isSaved = newVm.update(
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

            if isSaved:
                return HttpResponse('successful')
            else:
                return HttpResponse('failed')
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
            return render_to_response(
                'allMacs.html',
                {'macs': macs, 'freeMacs': freeMacs}
            )
        else:
            return HttpResponse('failed')


@csrf_exempt
@login_required
def renderAddIps(request):
    """
    渲染添加mac的对话框
    """
    if request.method == "POST":
        if request.POST.get('dialog', ''):
            vm = Vm(smart_str(request.POST.get('host')))
            ips = [ipOs.ipAddress for ipOs in vm.ip]
            allIpOs = Ip.objects.all()
            freeIps = [
                aIpOs.ipAddress for aIpOs in allIpOs if not aIpOs.instance
            ]
            return render_to_response(
                'allIps.html',
                {'ips': ips, 'freeIps': freeIps}
            )
        else:
            return HttpResponse('failed')


@csrf_exempt
@login_required
def renderChangeNode(request):
    """
    渲染添加mac的对话框
    """
    if request.method == "POST":
        if request.POST.get('dialog', ''):
            node = Vm(smart_str(request.POST.get('host'))).nodeHost
            allNodeOs = NodeHost.objects.all()
            allNodes = [
                aNodeOs.node
                for aNodeOs in allNodeOs
                if not aNodeOs.node == node
            ]
            return render_to_response(
                'allNodes.html',
                {'node': node, 'allNodes': allNodes}
            )
        else:
            return HttpResponse('failed')


@csrf_exempt
@login_required
def renderAddDogs(request):
    """
    渲染添加mac的对话框
    """
    if request.method == "POST":
        if request.POST.get('dialog', ''):
            thisVm = Vm(smart_str(request.POST.get('host')))
            vmDog = thisVm.dogSn
            vmNode = thisVm.nodeHost
            dogs = []
            for dogPort in vmDog:
                dogNP = {}
                dogNP['port'] = dogPort
                dogNP['sn'] = vmDog[dogPort]
                dogs.append(dogNP)
            thisNode = NodeHost.objects.get(node=vmNode)
            allDogOs = thisNode.usbport_set.all()
            freeDogs = [
                aDogOs.port for aDogOs in allDogOs if not aDogOs.instance
            ]
            return render_to_response(
                'allDogs.html',
                {'dogs': dogs, 'freeDogs': freeDogs}
            )
        else:
            return HttpResponse('failed')


@csrf_exempt
@login_required
def changeItems(request):
    """
    为某个实例修改node
    """
    if request.method == "POST":
        if request.POST.get('change', '') == u"node":
            thisVm = smart_str(request.POST.get('host'))
            oldValue = smart_str(request.POST.get('oldvalue', ''))
            newValue = smart_str(request.POST.get('newvalue', ''))
            vm = Vm(thisVm)
            try:
                vm.update(nodeHost=newValue)
                return HttpResponse('successful')
            except:
                return HttpResponse('failed')


@csrf_exempt
@login_required
def changeMacs(request):
    """
    为某个实例添加或删除mac
    """
    if request.method == "POST":
        hostName = request.POST.get('host', '')
        if not hostName:
            return HttpResponse('failed')
        else:
            oldMacs = request.POST.get('oldvalue', '')
            newMacs = request.POST.get('newvalue', '')
            oldMacsList = oldMacs.split(',')
            newMacsList = newMacs.split(',')
            try:
                thisHost = Instance.objects.get(instanceName=hostName)
                for aMac in oldMacsList:
                    if aMac.find(':') != -1:
                        thisMac = Mac.objects.get(macAddress=aMac)
                        thisMac.instance = None
                        thisMac.save()
                for aMac in newMacsList:
                    if aMac.find(':') != -1:
                        thisMac = Mac.objects.get(macAddress=aMac)
                        thisMac.instance = thisHost
                        thisMac.save()
                return HttpResponse('successful')
            except:
                return HttpResponse('failed')


@csrf_exempt
@login_required
def changeIps(request):
    """
    为某个实例添加或删除ip
    """
    if request.method == "POST":
        hostName = request.POST.get('host', '')
        if not hostName:
            return HttpResponse('failed')
        else:
            oldIps = request.POST.get('oldvalue', '')
            newIps = request.POST.get('newvalue', '')
            oldIpsList = oldIps.split(',')
            newIpsList = newIps.split(',')
            try:
                thisHost = Instance.objects.get(instanceName=hostName)
                for aIp in oldIpsList:
                    if aIp.find('.') != -1:
                        thisIp = Ip.objects.get(ipAddress=aIp)
                        thisIp.instance = None
                        thisIp.save()
                for aIp in newIpsList:
                    if aIp.find('.') != -1:
                        thisIp = Ip.objects.get(ipAddress=aIp)
                        thisIp.instance = thisHost
                        thisIp.save()
                return HttpResponse('successful')
            except:
                return HttpResponse('failed')


@csrf_exempt
@login_required
def changeDogs(request):
    """
    为某个实例添加或删除dog
    """
    if request.method == "POST":
        hostName = request.POST.get('host', '')
        oldDogs = request.POST.get('oldvalue', '')
        newDogs = request.POST.get('newvalue', '')
        oldDogsList = oldDogs.split(',')
        newDogsList = newDogs.split(',')

        try:
            thisHost = Instance.objects.get(instanceName=hostName)
        except:
            return HttpResponse('failed')
        if not hostName:
            return HttpResponse('failed')
        else:
            try:
                testDogNP = newDogsList[1].split(':')
                testDogP = testDogNP[0]
                if testDogP == '-':
                    thisPorts = UsbPort.objects.filter(instance=thisHost)
                    for aPort in thisPorts:     # 删除对应的sn
                        try:
                            aPort.dogsn.delete()
                            aPort.save()
                        except:
                            pass
                    for aPort in thisPorts:     # 取消和instance的关联
                        aPort.instance = None
                        aPort.save()
                    return HttpResponse('successful')
                else:
                    for dog in oldDogsList:
                        dogNP = dog.split(':')
                        try:
                            dogP = dogNP[0]
                            dogN = dogNP[1]
                        except:
                            continue
                        else:
                            try:
                                thisPort = UsbPort.objects.get(port=dogP)
                            except:
                                pass
                            else:
                                thisPort.instance = None
                                thisPort.dogsn.delete()
                                thisPort.save()
                    for dog in newDogsList:
                        dogNP = dog.split(':')
                        try:
                            dogP = dogNP[0]
                            dogN = dogNP[1]
                        except:
                            continue
                        else:
                            thisPort = UsbPort.objects.get(port=dogP)
                            try:
                                thisSn = DogSN.objects.create(
                                    sn=dogN,
                                    port=thisPort
                                )
                                thisSn.save()
                            except:
                                return HttpResponse('failed')
                            thisPort.instance = thisHost
                            thisPort.save()
                    return HttpResponse('successful')
            except:
                return HttpResponse('failed')
    else:
        return HttpResponse('404 not found')
