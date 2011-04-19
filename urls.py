# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('datasources.views',
    (r'^$', 'index', {}, 'index'),
)
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
