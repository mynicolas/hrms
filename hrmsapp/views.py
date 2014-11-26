#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from models import *


@login_required
@csrf_exempt
def renderVms(request):
	"""
	根据用户权限渲染实例项目
	"""
	if request.method == "POST":
		sendContent = getUserVms(request.user)
		return HttpResponse(sendContent)


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
				useInterval=request.POST.get('useinterval', ''),
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


@login_required
@csrf_exempt
def addIp(request):
	"""
	添加IP
	参数中带有需要添加的ip信息
	"""
	if request.method == "POST":
		try:
			addIps(request.POST.get('ips', ''))
			return HttpResponse('successful')
		except:
			return HttpResponse('failed')


@login_required
@csrf_exempt
def addNode(request):
	"""
	添加节点
	参数中带有需要添加的节点信息
	"""
	if request.method == "POST":
		try:
			addNodes(request.POST.get('nodes', ''))
			return HttpResponse('successful')
		except:
			return HttpResponse('failed')


@login_required
@csrf_exempt
def renderIpNode(request):
	"""
	获取并返回ip池中的所有ip
	param: request.POST['item']
		item: ip || node
	"""
	item = request.POST.get('item', '')
	if item == u'ip':
		ips = getIps()
		return HttpResponse(ips)
	elif item == u'node':
		nodes = getNodes()
		return HttpResponse(nodes)
