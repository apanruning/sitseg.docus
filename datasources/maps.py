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
    
    
    
    # Problem? :D
    rows = [(
                r.value_set.get(column__pk=column_geo).area, 
                r.value_set.get(column__pk=column_value).value
            ) 
            for r in datasource.row_set.all()]
    
    #si tuviese las areas !!!!! que bueno seria
    #no encuentro la forma de decidir si la columna de valor es un numero o no

    # esto es con numeros
    min_val = min(float(r[1]) for r in rows)
    max_val = max(float(r[1]) for r in rows)

    layer = Layer()
    colors = [] # este colors solo sirve para controlar, es de juguete
    for geo, value in rows:
        # si no fuera none esto andaria en teoria
        #area = geo.to_layer()
        #
        # la idea es que es un degrade donde 0 es el valor minimo y 1 el maximo
        color = int((float(value)-min_val)*255/(max_val-min_val))
        colors.append("#%x0000" % color) #tonalidades de rojo

        

        #aca hay que hacer un toque de ingenieria, porque hay que hacer que ponga
        #el color en el area en el javascript (area.js)
        
        #area.color = "#%x0000" % color
        #layer.elements.append(area)
               
    # con valores de texto los colores se podrian elegir al azar :D
    
    #para puntos: tarea al lector.
    
    return render(
        request,
        'map_view.html',
        {
            'colors': colors,
            'rows': rows,
            'datasource': datasource,
            'json_layer': {} # layer convertido a json
        }
    )


def zonemap():
    pass

def pointmap():
    pass
