# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource
from datasources.interface_r import *

def stats(request,id):
    datasource = DataSource.objects.get(pk=int(id))
    
    return render(
        request,
        'stats.html',
        {
            'datasource': datasource,
        }
    )

def graf_decided(request,id):
    values = request.POST['campo']
    column = list()
    for v in values: 
        column.append(Column.objects.get(pk=int(v)))
        
    graphics = {}
    
    if len(values) == 1:
        graphics = {
            'Cajas':'/plots/'+str(column[0].id)+'/boxplot',
            'Barras':'/plots/'+str(column[0].id)+'/bar',
            'Torta':'/plots/'+str(column[0].id)+'/pie',
            'Histograma':'/plots/'+str(column[0].id)+'/hist',
            'Stripchart':'/plots/'+str(column[0].id)+'/strip',
            'Densidad':'/plots/'+str(column[0].id)+'/density',
            'Puntos':'/plots/'+str(column[0].id)+'/density',
            'Pareto':'/plots/'+str(column[0].id)+'/pareto',
        }
    elif len(values) == 2:
        graphics = {}
    
    return render(
        request,
        'graph_options.html',
        {          
            'dataset':graphics,
        }
    )

def histplot(request,id):
    col = Column.objects.get(pk=int(id))
    values = Value.objects.filter(column=col.id)
    list_values = [v.cast_value() for v in values]
    vector = robjects.IntVector(list_values)
    #png(file=str(col.datasource.name)+"-"+str(col.name)+".png")
    suffix_dir = "media/graphics/"
    name_file = col.datasource.name+"-"+col.name+"-histograma"
    png(file=suffix_dir+name_file)
    graph = hist(vector,col='blue',nclass=10,main='Frecuencia de '+col.name,ylab='Frecuencias',xlab='Valores')
    g = {'name':str(name_file)}
    off()
    
    return render(
        request,
        'graphic.html',
        {          
            'graphic':g,
        }
    )

def boxplot(request,id):
    col = Column.objects.get(pk=int(id))
    values = Value.objects.filter(column=col.id)
    list_values = [v.cast_value() for v in values]
    vector = robjects.FloatVector(list_values)
    graph = boxplot(vector,vector)

    return render(
        request,
        'graphic.html',
        {          
            'graphic':graph.r_repr(),
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
