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
    (r'^datasource/(?P<datasource_id>\w+)/document/(?P<id>\w+)/geometry_append$', 'geometry_append', {}, 'geometry_append'),
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
    (r'^datasource/(?P<datasource_id>\w+)/plot/scatter$', 'scatter_plot', {}, 'scatter_plot'),

)

