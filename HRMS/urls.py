from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import view
from HRMSApp import urls
from userprofile import userUrls


urlpatterns = patterns(
    '',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', view.redirectLogin),
    url(r'^login/$', view.renderLogin),
    url(r'^logout/$', view.logout),
    url(r'^register/$', view.register),
    url(r'^checklogin/$', view.login),
    url(r'^index/$', view.renderIndex),
    url(r'^query/', include(urls)),
    url(r'^allusers/$', view.renderAllUsers),
    url(r'^modifyuseritem/$', view.modifyUserItem),
    url(r'^user/', include(userUrls)),
    url(r'^test/$', view.test),
)
