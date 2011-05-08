# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('datasources.views',
    (r'^$', 'index', {}, 'index'),
    (r'^datasource/download_attach$', 'download_attach', {}, 'download_attach'),    
)
