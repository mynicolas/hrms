from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import view
from HRMSApp import urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HRMS.views.home', name='home'),
    # url(r'^HRMS/', include('HRMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
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
    url(r'^test/$', view.test),
)
