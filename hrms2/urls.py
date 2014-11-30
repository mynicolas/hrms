#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views
from hrmsapp import urls as dataUrls
from userprofile import urls as profileUrls
from login import urls as loginUrls
from desk import urls as deskUrls

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include(loginUrls)),
    url(r'^', include(deskUrls)),
    url(r'^vm/', include(dataUrls)),
    url(r'^user/', include(profileUrls)),
)
