#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
import views

urlpatterns = patterns('',
    url(r'^all/$', views.renderAll),
    url(r'^ip/$', views.renderIp),
    url(r'^node/$', views.renderNode),
    url(r'^host/$', views.renderHost),
    url(r'^add/$', views.addHost),
    url(r'^addip/$', views.addIp),
    url(r'^log/$', views.renderLog),
    url(r'^logcondition/$', views.renderLogCondition),
    url(r'^companies/$', views.renderCompanies),
)
