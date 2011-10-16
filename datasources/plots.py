# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource
from datasources.interface_r import *

def stats(request,id):
    instance = Column.objects.get(pk=int(id))
    column_values = Column.objects.filter(datasource=instance.datasource)
    values = Value.objects.filter(column=instance.id)

    if not instance.has_geodata:
        #La columna no es geoposicionada        
        #aca deberian mostrarse n posibles estadisticas para los datos de esa columna
        #Se devuelve un diccionario en el contexto
        list_values = [v.cast_value() for v in values]

        vector_r = robjects.FloatVector(list_values)
        
        res = {
            'Numeros de Casos':length(vector_r)[0],
            'min':minimo(vector_r)[0],
            'max':maximo(vector_r)[0],
            'rango':(rango(vector_r)[0],rango(vector_r)[1]),
            'media':media(vector_r)[0],
            'varianza':cuasi_varianza(vector_r)[0],
            'desv_estandar':desviacion(vector_r)[0],
            'sumatoria':sumatoria(vector_r)[0],
        }
    else:
        res = values.order_by('value')
    
    return render(
        request,
        'stats.html',
        {
            'datasource': instance.datasource,
            'column':instance,
            'dataset': res,
        }
    )

def graf_decided(request,id):
    values = request.POST['campo']
    datasource = DataSource.objects.get(pk=int(request.POST['datasource']))
    column = list()
    for v in values: 
        column.append(Column.objects.get(pk=int(v)))
        
    graphics = {}
    
    if len(values) == 1:
        
        graphics = {
            'Boxplot':'/plots/'+str(datasource.id)+'/boxplot',
            'Torta':'/plots/'+str(datasource.id)+'/pie',
            'Histograma':'/plots/'+str(datasource.id)+'/hist',
        }
    
    return render(
        request,
        'graph_options.html',
        {          
            'dataset':graphics,
        }
    )

def histplot(request,id):
    return render(
        request,
        'graphic.html',
        {          
            'graphic':{},
        }
    )

def boxplot(request,id):
    return render(
        request,
        'graphic.html',
        {          
            'graphic':{},
        }
    )

def pieplot(request,id):
    return render(
        request,
        'graphic.html',
        {          
            'graphic':{},
        }
    )
