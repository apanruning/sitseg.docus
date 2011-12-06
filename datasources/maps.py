# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource, Out
from datasources.interface_r import *
from django import forms
from maap.models import MaapArea, MaapPoint


class CommentForm(forms.Form):
    column_geo = forms.ChoiceField(label='Columna Geoposicionada')
    column_value = forms.ChoiceField(label='Columna de Ponderación')
    datasource = forms.CharField(widget= forms.HiddenInput)
    
def map_form(request, id):
    #This function populate manager's graphic for produce Maps 
    #id is a parameter that represent the dataset id
   
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    columns = [(c.pk, c.name) for c in datasource.column_set.all()]
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
    datasource_id = request.POST['datasource']
    column_geo = request.POST['column_geo']
    column_value = request.POST['column_value']
    datasource = DataSource.objects.get(pk=datasource_id)
    
    
    
    return render(
        request,
        'map_view.html',
        {
            'datasource': datasource,
            'json_layer': {}
        }
    )


def zonemap():
    pass

def pointmap():
    pass
