# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('datasources.views',
    (r'^$', 'index', {}, 'index'),
    (r'^datasource/(?P<id>\w+)/$', 'detail', {}, 'detail'),        
    (r'^datasource/(?P<id>\w+)/download_attach$', 'download_attach', {}, 'download_attach'),    
    (r'^datasource/(?P<id>\w+)/autogenerate_columns$', 'autogenerate_columns', {}, 'autogenerate_columns'),    
    (r'^datasource/(?P<id>\w+)/import_data$', 'import_data', {}, 'import_data'),    
#    (r'^datasource/(?P<datasource_id>\w+)/document$', 'document_list', {}, 'document_list'),    
#    (r'^datasource/(?P<datasource_id>\w+)/document/add$', 'document_add', {}, 'document_add'),
#    (r'^datasource/(?P<datasource_id>\w+)/document/(?P<id>\w+)$', 'document_detail', {}, 'document_detail'),
#    (r'^datasource/(?P<datasource_id>\w+)/document/(?P<id>\w+)/edit$', 'document_edit', {}, 'document_edit'),
    (r'^datasource/(?P<datasource_id>\w+)/plot/scatter$', 'scatter_plot', {}, 'scatter_plot'),
    (r'^datasource/(?P<datasource_id>\w+)/document/(?P<id>\w+)/geometry_append$', 'geometry_append', {}, 'geometry_append'),
    (r'^datasource/(?P<id>\w+)/data$', 'show_data', {}, 'show_data'),    
    (r'^column/(?P<id>\w+)$', 'column', {}, 'column'),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    )
