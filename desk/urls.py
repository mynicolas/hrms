#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

from views import *
from userprofile import urls as userprofileUrls


urlpatterns = patterns(
    '',
    url(r'^$', renderDesk),
    url(r'^logout/$', logout),
    url(r'^user/',  include(userprofileUrls)),
)
