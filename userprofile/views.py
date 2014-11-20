#-*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from userprofile.models import Profile

@login_required
@csrf_exempt
def renderInstances(request):
	"""
	渲染当前用户的所有实例
	"""
	try:
		thisUser = request.user.get_profile()
		thisUser.instanceSort = request.POST['sort']
		thisUser.save()
		sendContent = "successful"
	except:
		sendContent = "failed"
	return HttpResponse(sendContent) 