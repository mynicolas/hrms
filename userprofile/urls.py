#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns(
    '',
    url('^$', renderAllUsers),
    url('^changeperm/$', changePerm),
)
