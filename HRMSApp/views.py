#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from getdata import *
from HRMSApp.models import *

"""
<xml>
    <aHost>
        <name></name>
        <core></core>
        <mem></mem>
        <disk></disk>
        <mac></mac>
        <start></start>
        <end></end>
        <company></company>
        <remotePort></remotePort>
        <dogN></dogN>
        <dogP></dogP>
        <bandwidth></bandwidth>
        <node></node>
        <ip></ip>
    </aHost>
    ...
</xml>
"""

@csrf_exempt
def renderAll(request):
    thisUser = request.user
    if request.method == 'POST':
        sendContent = "<xml>"
        companies = getAll(thisUser)
        if companies == 'empty':
            return HttpResponse('empty')
        for aCompany in companies:
            companyName = aCompany['companyName']
            _instances = aCompany['instances']
            for instance in _instances:
                sendContent += "<aHost>" +\
                "<name>" + instance['instanceName'] + "</name>" +\
                "<core>" + instance['core'] + "</core>" +\
                "<mem>" + instance['mem'] + "</mem>" +\
                "<disk>" + instance['dataDisk'] + "</disk>" +\
                "<mac>" + instance['macAddress'] + "</mac>" +\
                "<start>" + instance['startDate'] + "</start>" +\
                "<end>" + instance['useInterval'] + "</end>" +\
                "<bandwidth>" + instance['bandwidth'] + "</bandwidth>" +\
                "<company>" + companyName + "</company>" +\
                "<remotePort>" + instance['remotePort'] + "</remotePort>" +\
                "<ip>" + instance['ip'] + "</ip>" +\
                "<dogN>" + instance['dogSn'] + "</dogN>" +\
                "<dogP>" + instance['dogPort'] + "</dogP>" +\
                "<node>" + instance['nodeName'][0] + "</node></aHost>"

        sendContent += "</xml>"
        return HttpResponse(sendContent)
    else:
        return HttpResponse("not found")

@csrf_exempt
def renderIp(request):
    """
    当前端点击ip的下拉框时，request包含一个键（host = hostName），本函数用来选来渲染下拉列表，从数据库中传出所有状态为未使用的ip
    当前端选择某个ip时，request包含三个键（host = hostName, originalIp = oldIp, newIp = ip）本函数用来将原ip的状态设置为未使用，将新ip设置为已使用
    """
    try:
        hostName = smart_str(request.POST['hostName'])
    except:
        hostName = False
    try:
        originalIp = smart_str(request.POST['originalIp'])
    except:
        originalIp = False
    try:
        newIp = smart_str(request.POST['newIp'])
    except:
        newIp = False
    if hostName and not originalIp and not newIp:
        sendContent = "<xml>"
        ips = getAllNotUsedIp()
        for ip in ips:
            sendContent += "<ip>" + ip + "</ip>"
        sendContent += "</xml>"

    elif hostName and originalIp and newIp:
        host = Instance.objects.get(instanceName = hostName)
        host.ip = newIp
        host.save()
        isSaved = setIp(originalIp, newIp)
        if isSaved:
            sendContent = "successful"

            saveLog("%s change IP '%s' to '%s'" %(hostName, originalIp, newIp))
        else:
            sendContent = "error"
    else:
        sendContent = "error"

    return HttpResponse(sendContent)

@csrf_exempt
def renderNode(request):
    """
    当前端点击node的下拉框时，request包含一个键（host = hostName），本函数用来选来渲染下拉列表，从数据库中传出所有状态为未使用的ip
    当前端选择某个node时，request包含三个键（host = hostName, originalIp = oldIp, newIp = ip）本函数用来将原ip的状态设置为未使用，将新ip设置为已使用
    """
    pass

@csrf_exempt
def renderHost(request):
    """
    修改主机的可修改元素
    request.POST中包含三个键
    hostName: 主机名，对应数据库中的Instance表中的instanceName
    hostElement: 对应数据库中的Instance表中的除了instanceName, dogSn, dogPort, node, ip, company的其他字段
    data: 修改后的数据，将元数据修改为data
    """
    if request.method == 'POST':
        hostName = smart_str(request.POST['hostName'])
        hostElement = smart_str(request.POST['hostElement'])
        data = smart_str(request.POST['data'])
        isSaved = hostElementMap(hostName, hostElement, data)

        saveLog("The '%s' of virtual machine '%s' was changed to '%s'" % (hostElement, hostName, data))
        return HttpResponse(isSaved)
    else:
        saveLog()
        return HttpResponse("not found")

@csrf_exempt
def addHost(request):
    """
    添加虚拟主机
    """
    if request.method == "POST":
        thisUser = request.user
        name = smart_str(request.POST['hostName'])
        core = smart_str(request.POST['hostCore'])
        mem = smart_str(request.POST['hostMem'])
        disk = smart_str(request.POST['hostDisk'])
        mac = smart_str(request.POST['hostMac'])
        start = smart_str(request.POST['hostStart'])
        end = smart_str(request.POST['hostEnd'])
        company = smart_str(request.POST['hostCompany'])
        remotePort = smart_str(request.POST['hostRemotePort'])
        dogN = smart_str(request.POST['hostDogN'])
        dogP = smart_str(request.POST['hostDogP'])
        bandwidth = smart_str(request.POST['hostBandwidth'])
        node = smart_str(request.POST['hostNode'])
        ip = smart_str(request.POST['hostIp'])

        sendContent = addNewHost(thisUser, name,
                                    hostCore = core,
                                    hostMem = mem,
                                    hostDisk = disk,
                                    hostMac = mac,
                                    hostStart = start,
                                    hostEnd = end,
                                    hostCompany = company,
                                    hostRemotePort = remotePort,
                                    hostDogN = dogN,
                                    hostDogP = dogP,
                                    hostBandwidth = bandwidth,
                                    hostNode = node,
                                    hostIp = ip)

        if sendContent == 'successful':
            saveLog("The new virtual machine '%s' was created" % name)
    else:
        sendContent = "error"
    return HttpResponse(sendContent)

@csrf_exempt
def addIp(request):
    """
    获取post数据，得到IP列表，并将列表中的IP逐个存入数据库中的IP表
    """
    if request.method == "POST":
        ips = smart_str(request.POST['ips']).split(',')
        isSave = saveIps(*ips)
        return HttpResponse(isSave)
    else:
        return HttpResponse('error')


@csrf_exempt
def renderLog(request):
    """
    渲染log视图
    """
    if request.method == "POST":
        logList = getLog()
        sendContent = "<xml>"
        for log in logList:
            sendContent += "<log>" + log + "</log>"
        sendContent += "</xml>"
    else:
        sendContent = "error"

    return HttpResponse(sendContent)

@csrf_exempt
def renderLogCondition(request):
    if request.method == "POST":
        logs = []
        condition = smart_str(request.POST['condition'])
        if condition == 'time':
            # global logs
            interval = smart_str(request.POST['interval'])
            hostName = smart_str(request.POST['hostname'])
            logs = conditionLog(condition, hostName = hostName, interval = interval)

        elif condition == 'hostname':
            # global logs
            logs = conditionLog(condition)

        sendContent = "<xml>"
        for log in logs:
            sendContent += "<log>" + log + "</log>"
        sendContent += "<xml>"
    else:
        sendContent = 'error'
    return HttpResponse(sendContent)

# # 处理usb的post请求
# # return当前用户所有usb
# @csrf_exempt
# def renderItems(request):
#     host = {'name': 'name1',
#             'core': '4',
#             'mem': '16',
#             'disk': '12',
#             'mac': '74:2F:68:7F:CF:F6',
#             'start': 'start1',
#             'end': 'end1',
#             'company': 'company1',
#             'remotePort': '33333',
#             'dogN': 'dogN1',
#             'dogP': 'dogP1',
#             'bandwidth': '10',
#             'node': '255.255.255.253',
#             'ip': '255.255.255.254'}
#     host1 = {'name': 'name2',
#             'core': '8',
#             'mem': '8',
#             'disk': '1025',
#             'mac': '74:2F:68:7F:CF:F7',
#             'start': 'start2',
#             'end': 'end2',
#             'company': 'company2',
#             'remotePort': '66666',
#             'dogN': 'dogN2',
#             'dogP': 'dogP2',
#             'bandwidth': '1',
#             'node': '255.255.255.252',
#             'ip': '255.255.255.255'}
#     hosts = [host, host1]
#     if request.method == "POST":
#         sendContent = "<xml>"
#         for aHost in hosts:
#             sendContent += "<aHost>"
#             for item in aHost:
#                 sendContent += "<%s>%s</%s>" % (item, aHost[item], item)
#             sendContent += "</aHost>"
#         sendContent += "</xml>"
#         return HttpResponse(sendContent)
#     else:
#         return HttpResponse("not found")

# @csrf_exempt
# # 处理ip的post请求
# # return当前用户所有Ip
# def renderIp(request):
#     """
#         <xml>
#             <ip>
#                 'ip'
#             </ip>
#             ...
#         </xml>
#     """
#     ip1 = [
#         '111.111.111.111',
#         '222.222.222.222'
#     ]
#     ip2 = [
#         '122.122.122.122',
#         '221.221.221.221',
#         '121.121.121.121'
#     ]
#     ips = {'vm001': ip1, 'vm002': ip2}
#
#     if request.method == 'POST':
#         hostName = request.POST['host']
#         sendContent = "<xml>"
#         for ip in ips[hostName]:
#             sendContent += "<ip>" + ip + "</ip>"
#         sendContent += "</xml>"
#         return  HttpResponse(sendContent)

# @csrf_exempt
# # 处理node的post请求
# # return当前用户所有node
# def renderNode(request):
#     """
#         <xml>
#             <node>
#                 'ip'
#             </node>
#             ...
#         </xml>
#     """
#     node1 = [
#         '101.102.103.104',
#         '201.202.203.204'
#     ]
#     node2 = [
#         '102.103.104.105',
#         '202.203.204.205'
#     ]
#     nodes = {'vm001': node1, 'vm002': node2}
#
#     if request.method == 'POST':
#         hostName = request.POST['host']
#         sendContent = "<xml>"
#         for node in nodes[hostName]:
#             sendContent += "<node>" + node + "</node>"
#         sendContent += "</xml>"
#         return HttpResponse(sendContent)



