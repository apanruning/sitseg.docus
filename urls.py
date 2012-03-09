# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from datasources import models

admin.autodiscover()

urlpatterns = patterns('datasources.views',
    (r'^$', 'index', {}, 'index'),

    (r'^dataset/(?P<id>\w+)/$', 'dataset_detail', {}, 'dataset_detail'),
    (r'^dataset/(?P<id>\w+)/delete', 'delete', {'model':models.DataSet}),

    (r'^datasource/(?P<id>\w+)/$', 'datasource_detail', {}, 'datasource_detail'),
    (r'^datasource/(?P<id>\w+)/delete$', 'delete', {'model':models.DataSource}),

    (r'^datasource/(?P<id>\w+)/download_attach_source$', 'download_attach_source', {}, 'download_attach_source'),
    (r'^datasource/(?P<id>\w+)/download_attach_geom$', 'download_attach_geom', {}, 'download_attach_geom'),
    (r'^datasource/(?P<id>\w+)/import_data$', 'import_data', {}, 'import_data'),
    (r'^datasource/(?P<id>\w+)/show_data', 'show_data', {}, 'show_data'),
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
    #Funciones que arman el formulario para graficar
    (r'^plots/(?P<id>\w+)/hist$', 'histplot', {}, 'histplot'),
    (r'^plots/(?P<id>\w+)/box$', 'box', {}, 'box'),
    (r'^plots/(?P<id>\w+)/pie$', 'pieplot', {}, 'pieplot'),
    (r'^plots/(?P<id>\w+)/bar$', 'barplot', {}, 'barplot'),
    (r'^plots/(?P<id>\w+)/scatter$', 'scatter', {}, 'scatter'),
    (r'^plots/(?P<id>\w+)/scattermatrix$', 'scattermatrix', {}, 'scattermatrix'),
    (r'^plots/(?P<id>\w+)/stripchart$', 'stripchart', {}, 'stripchart'),
    (r'^plots/(?P<id>\w+)/density$', 'density', {}, 'density'),
    (r'^plots/(?P<id>\w+)/map_point_density$', 'map_point_density_form', {}, 'map_point_density_form'),
        
    #Funciones que grafican (se conectan directamente con R)
    (r'^graph/scatterplot$', 'scatterplot_view', {}, 'scatterplot_view'),
    (r'^graph/scatterplotmatrix$', 'scatterplotmatrix_view', {}, 'scatterplotmatrix_view'),
    (r'^graph/histogram$', 'histogram_view', {}, 'histogram_view'),
    (r'^graph/boxplot$', 'boxplot_view', {}, 'boxplot_view'),
    (r'^graph/stripchart$', 'stripchart_view', {}, 'stripchart_view'),
    (r'^graph/pieplot$', 'pieplot_view', {}, 'pieplot_view'),
    (r'^graph/densityplot$', 'densityplot_view', {}, 'densityplot_view'),
    (r'^graph/barplot$', 'barplot_view', {}, 'barplot_view'),
    (r'^graph/map_point_density$', 'map_point_density_view', {}, 'map_point_density_view'),

    (r'^outqueue$', 'outqueue', {}, 'outqueue'),
)

urlpatterns += patterns('datasources.maps',
    (r'^plots/(?P<id>\w+)/map_density_area$', 'density_by_area_form', {}, 'density_by_area_form'),
    (r'^graph/density_by_area_plot$', 'density_by_area_view', {}, 'density_by_area_view'),
    (r'^plots/(?P<id>\w+)/map_points','map_points_form',{}, 'map_points_form'),
    (r'^graph/map_points_plot$', 'map_points_view', {}, 'map_points_view'),
    (r'^plots/(?P<id>\w+)/dist_by_area','dist_by_area_form',{}, 'dist_by_area_form'),
    (r'^graph/dist_by_area_plot$', 'dist_by_area_view', {}, 'dist_by_area_view'),
    (r'^plots/(?P<id>\w+)/map_area_r$', 'map_area_r_form', {}, 'map_area_r_form'),
    (r'^graph/map_area_r_plot$', 'map_area_r_view', {}, 'map_area_r_view'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    )
