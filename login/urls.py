#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns(
    '',
    url(r'^$', renderLogin),
    url(r'^register/$', register),
    url(r'checkuser/$', checkUser),
    url(r'^check/$', checkLogin),
)
