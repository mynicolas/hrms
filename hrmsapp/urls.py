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
    url(r'^owners/$', renderOwners),
    url(r'^addnode/$', addNode),
    url(r'^addip/$', addIp),
    url(r'^addowner/$', addOwner),
    url(r'^adddog/$', addDogPort),
    url(r'^addmac/$', addMac),
    url(r'^modify/$', modify),
    url(r'^addmacdialog/$', renderAddMacs),
    url(r'^addipdialog/$', renderAddIps),
    url(r'^adddogdialog/$', renderAddDogs),
    url(r'^changenodedialog/$', renderChangeNode),
    url(r'^changeownerdialog/$', renderChangeOnwer),
    url(r'^changenode/$', changeNode),
    url(r'^changemacs/$', changeMacs),
    url(r'^changeips/$', changeIps),
    url(r'^changedogs/$', changeDogs),
)
