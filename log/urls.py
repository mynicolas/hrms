#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns(
    '',
    url(r'^$', renderLogs),
    url(r'^conditionlog/$', conditionLog),
)
