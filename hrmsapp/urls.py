#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns(
	'',
	url(r'^$', renderVms),
	url(r'^add/$', addHost),
	url(r'^addip/$', addIp),
	url(r'^addnode/$', addNode),
	url(r'^renderip/$', renderIpNode),
)
