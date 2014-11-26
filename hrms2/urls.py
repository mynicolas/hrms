#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import views
from hrmsapp import urls as dataUrls
from userprofile import urls as profileUrls
from login import urls as loginUrls

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', include(loginUrls)),
    url(r'^$', views.renderIndex),
    url(r'^vm/', include(dataUrls)),
    url(r'^user/', include(profileUrls)),
)
