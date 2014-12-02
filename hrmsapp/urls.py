#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns(
    '',
    url(r'^$', renderVms),
    url(r'^add/$', addHost),
    url(r'^nodes/$', renderNodes),
    url(r'^dogports/$', renderDogPorts),
    url(r'^ips/$', renderIps),
    url(r'^macs/$', renderMacs),
    url(r'^addnode/$', addNode),
    url(r'^addip/$', addIp),
    url(r'^adddog/$', addDogPort),
    url(r'^addmac/$', addMac),
    url(r'^modify/$', modify),
    url(r'^addmacdialog/$', renderAddMacs),
)
