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
    #Funciones que arman el formulario para graficar segun el grafico
    (r'^plots/(?P<id>\w+)/hist$', 'histplot', {}, 'histplot'),
    (r'^plots/(?P<id>\w+)/box$', 'box', {}, 'box'),
    (r'^plots/(?P<id>\w+)/pie$', 'pieplot', {}, 'pieplot'),
    (r'^plots/(?P<id>\w+)/bar$', 'barplot', {}, 'barplot'),
    (r'^plots/(?P<id>\w+)/scatter$', 'scatter', {}, 'scatter'),
    (r'^plots/(?P<id>\w+)/scattermatrix$', 'scattermatrix', {}, 'scattermatrix'),
    (r'^plots/(?P<id>\w+)/stripchart$', 'stripchart', {}, 'stripchart'),
    (r'^plots/(?P<id>\w+)/density$', 'density', {}, 'density'),
    
    #Funciones que grafican (se conectan directamente con R)
    (r'^graph/scatterplot$', 'scatterplot_view', {}, 'scatterplot_view'),
    (r'^graph/scatterplotmatrix$', 'scatterplotmatrix_view', {}, 'scatterplotmatrix_view'),
    (r'^graph/histogram$', 'histogram_view', {}, 'histogram_view'),
    (r'^graph/boxplot$', 'boxplot_view', {}, 'boxplot_view'),
    (r'^graph/stripchart$', 'stripchart_view', {}, 'stripchart_view'),
    (r'^graph/pieplot$', 'pieplot_view', {}, 'pieplot_view'),
    (r'^graph/densityplot$', 'densityplot_view', {}, 'densityplot_view'),
    (r'^graph/barplot$', 'barplot_view', {}, 'barplot_view'),

    (r'^outqueue$', 'outqueue', {}, 'outqueue'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    )
