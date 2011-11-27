# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from datasources import models

admin.autodiscover()

urlpatterns = patterns('datasources.views',
    (r'^$', 'workspace', {}, 'workspace'),
    (r'^workspace/$', 'workspace', {}, 'workspace'),
    (r'^workspace/(?P<id>\w+)/$', 'workspace_detail', {}, 'workspace_detail'),
    (r'^workspace/(?P<id>\w+)/delete', 'delete', {'model':models.Workspace}),

    (r'^dataset/(?P<id>\w+)/$', 'dataset_detail', {}, 'dataset_detail'),
    (r'^dataset/(?P<id>\w+)/delete', 'delete', {'model':models.DataSet}),

    (r'^datasource/(?P<id>\w+)/$', 'datasource_detail', {}, 'detail'),
    (r'^datasource/(?P<id>\w+)/get$', 'datasource_get', {}, 'datasource_get'),
    (r'^datasource/(?P<id>\w+)/delete$', 'delete', {'model':models.DataSource}),

    (r'^datasource/(?P<id>\w+)/download_attach$', 'download_attach', {}, 'download_attach'),
    (r'^datasource/(?P<id>\w+)/import_data$', 'import_data', {}, 'import_data'),

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
    (r'^plots/(?P<id>\w+)/hist$', 'histplot', {}, 'histplot'),
    (r'^plots/(?P<id>\w+)/box$', 'boxplot', {}, 'boxplot'),
    (r'^plots/(?P<id>\w+)/pie$', 'pieplot', {}, 'pieplot'),
    (r'^plots/(?P<id>\w+)/scatter$', 'scatterplot', {}, 'scatterplot'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    )
