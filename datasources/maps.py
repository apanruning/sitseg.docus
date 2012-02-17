# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource, Out
from datasources.interface_r import *
from django import forms
from maap.models import MaapArea, MaapPoint
from maap.layers import Layer

class CommentForm(forms.Form):
    column_geo = forms.ChoiceField(label='Columna Geoposicionada')
    column_value = forms.ChoiceField(label='Columna de Ponderación')
    datasource = forms.CharField(widget=forms.HiddenInput)
    
def map_form(request, id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=False)]
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True)]
    form = CommentForm({'datasource':id})
    form.fields['column_value'].choices = columns
    form.fields['column_geo'].choices = geo_columns

    return render(
        request,
        'map.html',
        {
            'datasource': datasource,
            'form':form,
            'action':'/graph/mapplot',
        }
    )

def mapplot_view(request):
    datasource_id = request.POST.get('datasource')
    column_geo = request.POST.get('column_geo')
    column_value = request.POST.get('column_value')
    
    datasource = DataSource.objects.get(pk=datasource_id)
    

    # Problem? :D
    rows = [(r.value_set.get(column__pk=column_geo).area,r.value_set.get(column__pk=column_value).value) 
            for r in datasource.row_set.all()]

    #Assume that column has only numbers
    
    areas = {}

    for geo, value in rows:
        if geo:
            if geo.pk in areas.keys():
                areas[geo.pk]['total'] += float(value)
            else:
                areas[geo.pk] = {
                    'total':float(value),
                    'geo': geo.to_geo_element(),
                }

    min_val = min(r['total'] for r in areas.itervalues())
    max_val = max(r['total'] for r in areas.itervalues())

    layer = Layer()
    for area in areas.itervalues():
        color = int((area['total']-min_val)*256/(max_val-min_val))-1
        area['geo'].color = "#%x0000" % color
        area['geo'].name = "%s (%d)" %(area['geo'].name, area['total']  ) 
        layer.elements.append(area['geo'])
                   
    return render(
        request,
        'map_view.html',
        {
            #'colors': colors,
            'rows': areas,
            'datasource': datasource,
            'json_layer': layer.json 
        }
    )


def zonemap():
    pass

def pointmap():
    pass
