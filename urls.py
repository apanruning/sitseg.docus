# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('datasources.views',
    (r'^$', 'index', {}, 'index'),
    (r'^datasource/(?P<id>\w+)/$', 'detail', {}, 'detail'),        
    (r'^datasource/(?P<id>\w+)/download_attach$', 'download_attach', {}, 'download_attach'),    
    (r'^datasource/(?P<id>\w+)/autogenerate_columns$', 'autogenerate_columns', {}, 'autogenerate_columns'),    
    (r'^datasource/(?P<id>\w+)/import_data$', 'import_data', {}, 'import_data'),    
    (r'^datasource/(?P<id>\w+)/data$', 'show_data', {}, 'show_data'),    

)
