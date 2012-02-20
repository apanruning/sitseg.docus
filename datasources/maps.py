# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource, Out
from datasources.interface_r import *
from django import forms
from maap.models import MaapArea, MaapPoint
from maap.layers import Layer
from django.db.models import Count

class CommentForm(forms.Form):
    column_geo = forms.ChoiceField(label='Variable')
    datasource = forms.CharField(widget=forms.HiddenInput)
    
def density_by_area_form(request, id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True)]
    form = CommentForm({'datasource':id})
    form.fields['column_geo'].choices = geo_columns

    return render(
        request,
        'map.html', 
        {
            'datasource': datasource,
            'form':form,
            'action':'/graph/density_by_area_plot',
        }
    )

def density_by_area_view(request):
    datasource_id = request.POST.get('datasource')
    column_geo = request.POST.get('column_geo')
    
    datasource = DataSource.objects.get(pk=datasource_id)
    flag = Column.objects.get(pk=column_geo).data_type

    if flag == 'area':
        areas = Value.objects.filter(column__datasource=datasource_id,column=column_geo).values("area").annotate(Count('area')).order_by()
    else:
          areas = Value.objects.filter(column__datasource=datasource_id,column=column_geo).values("point").annotate(Count('point')).order_by()      

    min_val = 0
    max_val = 1023

    layer = Layer()
    for area in areas:
        if flag == 'area':
            if area['area']:
                maap_area = MaapArea.objects.get(pk=area['area'])
                area['geo'] = maap_area.to_geo_element()
                color = int((area['area__count']-min_val)*256/(max_val-min_val))-1
                area['geo'].color = "#%x0000" % color
                area['geo'].name = "%s (%d)" %(maap_area.name, area['area__count']) 
                layer.elements.append(area['geo'])
        else:
            if area['point']:            
                maap_point = MaapPoint.objects.get(pk=area['point'])                   
                area['geo'] = maap_point.to_geo_element()
                color = int((area['point__count']-min_val)*256/(max_val-min_val))-1
                area['geo'].color = "#%x0000" % color
                area['geo'].name = "%s (%d)" %(maap_point.name, area['point__count']) 
                layer.elements.append(area['geo'])
        

    return render(
        request,
        'map_density_area.html',
        {
            #'colors': colors,
            'rows': areas,
            'datasource': datasource,
            'json_layer': layer.json, 
            'column_geo':Column.objects.get(pk=column_geo).name
        }
    )

def zonemap():
    pass

def pointmap():
    pass

