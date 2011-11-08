# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource
from datasources.interface_r import *

def stats(request,id):
    datasource = DataSource.objects.get(pk=int(id))
    plots_function = {
            'Cajas':'/plots/'+str(column[0].id)+'/boxplot',
            'Barras':'/plots/'+str(column[0].id)+'/bar',
            'Torta':'/plots/'+str(column[0].id)+'/pie',
            'Histograma':'/plots/'+str(column[0].id)+'/hist',
            'Stripchart':'/plots/'+str(column[0].id)+'/strip',
            'Densidad':'/plots/'+str(column[0].id)+'/density',
            'Puntos':'/plots/'+str(column[0].id)+'/density',
            'Pareto':'/plots/'+str(column[0].id)+'/pareto',
            
            
        }

    return render(
        request,
        'stats.html',
        {
            'plots':plots_function,            
            'datasource': datasource,
        }
    )

def histplot(request,id):
    col = Column.objects.get(pk=int(id))
    values = Value.objects.filter(column=col.id)
    list_values = [v.cast_value() for v in values]
    vector = robjects.IntVector(list_values)
    suffix_dir = "media/graphics/"
    name_file = col.datasource.name+"-"+col.name+"-histograma"
    ext_file = ".png"
    png(file=suffix_dir+name_file+ext_file)
    graph = hist(vector,col='blue',nclass=10,main='Frecuencia de '+col.name,ylab='Frecuencias',xlab='Valores')
    g = {'name':str(name_file+ext_file)}
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
    suffix_dir = "media/graphics/"
    name_file = col.datasource.name+"-"+col.name+"-histograma"
    ext_file = ".png"
    png(file=suffix_dir+name_file+ext_file)
    graph = boxplot(vector,vector)
    g = {'name':str(name_file+ext_file)}
    off()

    return render(
        request,
        'graphic.html',
        {          
            'graphic':g,
        }
    )

def pieplot(request,id):
    col = Column.objects.get(pk=int(id))
    values = Value.objects.filter(column=col.id)
    list_values = [v.cast_value() for v in values]
    vector = robjects.FloatVector(list_values)
    suffix_dir = "media/graphics/"
    name_file = col.datasource.name+"-"+col.name+"-torta"
    ext_file = ".png"
    png(file=suffix_dir+name_file+ext_file)
    graph = piechart(x, labels=names(x), shadow=FALSE,edges=200, radius=0.8, col=NULL, main="Grafico de Torta para %s" %(col.name))
    g = {'name':str(name_file+ext_file)}
    off()
    return render(
        request,
        'graphic.html',
        {          
            'graphic':g,
        }
    )
