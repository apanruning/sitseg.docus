# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('datasources.views',
    (r'^$', 'datasource', {}, 'index'),
    (r'^datasource/(?P<id>\w+)/$', 'datasource_detail', {}, 'detail'),
    (r'^datasource/(?P<id>\w+)/download_attach$', 'download_attach', {}, 'download_attach'),
    (r'^datasource/(?P<id>\w+)/import_data$', 'import_data', {}, 'import_data'),
    (r'^datasource/(?P<id>\w+)/data$', 'show_data', {}, 'show_data'),
    (r'^column/(?P<id>\w+)$', 'column_detail', {}, 'column'),
   
)

urlpatterns += patterns('django.contrib.auth.views',
    (r'login$', 'login', {'template_name':'login.html'}),
    (r'logout$', 'logout'),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('datasources.plots',
    (r'^plots/(?P<id>\w+)$', 'stats', {}, 'stats'),
    (r'^plots/(?P<id>\w+)/graph$', 'graf_decided', {}, 'graf_decided'),
    (r'^/plots/(?P<id>\w+)/hist$', 'histplot', {}, 'histplot'),
    (r'^/plots/(?P<id>\w+)/boxplot$', 'boxplot', {}, 'boxplot'),
    (r'^/plots/(?P<id>\w+)/pie$', 'pieplot', {}, 'pieplot'),
)

