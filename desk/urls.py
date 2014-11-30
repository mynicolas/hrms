#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

from views import *


urlpatterns = patterns(
    '',
    url(r'^$', renderDesk),
    url(r'^logout/$', logout),
)
