# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource, Out
from datasources.interface_r import *
from django import forms

def histplot(request,id):
    #This function populate manager's graphic for produce Histogram 
    #id is a parameter that represent the dataset id
   
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
   
    options = {
                'labels':['Seleccione Variable'],
                'action':'/graph/histogram',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
        }
    )

def box(request,id):
    #This function populate manager's graphic for produce Histogram 
    #id is a parameter that represent the dataset id
   
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
   
    options = {
                'labels':['Seleccione Variable'],
                'action':'/graph/boxplot',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
        }
    )

def scatter(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable','Seleccione Variable','Seleccione'],
        'action':'/graph/scatterplot',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
        }
    )

def scattermatrix(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable','Seleccione Variable'],
        'action':'/graph/scatterplotmatrix',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
        }
    )

def stripchart(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable'],
        'action':'/graph/stripchart',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
        }
    )

def pieplot(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable'],
        'action':'/graph/pieplot',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
        }
    )

def density(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable'],
        'action':'/graph/densityplot',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
        }
    )

def barplot(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable'],
        'action':'/graph/barplot',
    }
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
        }
    )

#Funciones que graficar (se conectan directamente con R)
def histogram_view(request):
    if request.method == "POST":
        var = request.POST['var-0']
        
        #configuracion para tipo de archivo donde se guarda el grafico y nombre del mismo
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        name_file = "histograma"+var
        png(file=suffix_dir+name_file+ext_file)
        
        #se preparan los valores. TODO: Refactorizar casteo. Hacer mas eficiente. 
        values = Value.objects.filter(column=var)
        list_values = [v.cast_value() for v in values]
        
        #creacion de vector R con los valores correspondientes (R)     
        vector = robjects.FloatVector(list_values)

        #parametros del grafico
        freq = False
        probability = not freq
        include = True
        right = True
        col = "blue"
        border = par("fg")

        main = "Histograma de %s" %(Column.objects.get(pk=var).name)
        xlab = "Valores"
        ylab = "Frecuencia"

        hist(vector,col=col,border=border,main=main,xlab=xlab,ylab=ylab)
        off()

        #Guardo el resultado y lo muestro en la cola de salida
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def boxplot_view(request):
    if request.method == "POST":
        var = request.POST['var-0']

        #configuracion para tipo de archivo donde se guarda el grafico y nombre del mismo
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        name_file = "cajas"+var
        png(file=suffix_dir+name_file+ext_file)

        #se preparan los valores. TODO: Refactorizar casteo. Hacer mas eficiente. 
        values = Value.objects.filter(column=var)
        list_values = [v.cast_value() for v in values]
        
        #creacion de vector R con los valores correspondientes (R)     
        vector = robjects.FloatVector(list_values)

        #parametros del grafico
        jitter=0.1 
        offset=1/3
        vertical=True
        #group.names
        #xlim=NULL 
        #ylim=NULL
        main=Column.objects.get(pk=var).name
        ylab=""
        xlab="Valores"
        pch=1
        col=par("fg")
        cex=par("cex")

        boxplot(vector)
        off()
     
        #Guardo el resultado y lo muestro en la cola de salida
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def stripchart_view(request):
    if request.method == "POST":
        var = request.POST['var-0']
        
        #configuracion para tipo de archivo donde se guarda el grafico y nombre del mismo
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        name_file = "stripchart"+var
        png(file=suffix_dir+name_file+ext_file)

        #se preparan los valores. TODO: Refactorizar casteo. Hacer mas eficiente. 
        values = Value.objects.filter(column=var)
        list_values = [v.cast_value() for v in values]
        
        #creacion de vector R con los valores correspondientes (R)     
        vector = robjects.FloatVector(list_values)

        #parametros del grafico
        jitter=0.1 
        offset=1/3
        vertical=True
        #group.names
        #xlim=NULL 
        #ylim=NULL
        main=Column.objects.get(pk=var).name
        ylab=""
        xlab="Valores"
        pch=1
        col=par("fg")
        cex=par("cex")

        strip(list_values,method="overplot",jitter=jitter,offset=offset,vertical=vertical,main=main,xlab=xlab,pch=pch,col=col,cex=cex)
        off()
     
        #Guardo el resultado y lo muestro en la cola de salida
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def scatterplot_view(request):
    if request.method == "POST":
        var1 = request.POST['var-0']
        var2 = request.POST['var-1']
        
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        
        values_var1 = Value.objects.filter(column=var1)
        values_var2 = Value.objects.filter(column=var2)

        list_values_var1 = [v.cast_value() for v in values_var1]
        list_values_var2 = [v.cast_value() for v in values_var2]
        errors=""

        #configuracion para el grafico     
        try:
            vector_var1 = robjects.FloatVector(list_values_var1)
            vector_var2 = robjects.FloatVector(list_values_var2)
        except e:
            errors = e

        name_file = "scatter"+var1+var2
        png(file=suffix_dir+name_file+ext_file)
        scatterplot(vector_var1, vector_var2)
        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def scatterplotmatrix_view(request):
    if request.method == "POST":
        var1 = request.POST['var-0']
        var2 = request.POST['var-1']
        
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        
        values_var1 = Value.objects.filter(column=var1)
        values_var2 = Value.objects.filter(column=var2)

        list_values_var1 = [v.cast_value() for v in values_var1]
        list_values_var2 = [v.cast_value() for v in values_var2]
        errors=""

        #configuracion para el grafico     
        try:
            vector_var1 = robjects.FloatVector(list_values_var1)
            vector_var2 = robjects.FloatVector(list_values_var2)
        except e:
            errors = e


        main=Column.objects.get(pk=var1).name+'-'+Column.objects.get(pk=var2).name
        ylab=""
        xlab="Valores"


        name_file = "scatterplotmatrix"+var1+var2
        png(file=suffix_dir+name_file+ext_file)
        scatterplotmatrix([vector_var1, vector_var2])
        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def densityplot_view(request):
    if request.method == "POST":
        var1 = request.POST['var-0']
        
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        
        values_var1 = Value.objects.filter(column=var1)

        list_values_var1 = [v.cast_value() for v in values_var1]
        
        errors=""
        #configuracion para el grafico     
        try:
            vector_var1 = robjects.FloatVector(list_values_var1)
        
        except e:
            errors = e

        name_file = "density"+var1
        png(file=suffix_dir+name_file+ext_file)

        densityplot(vector_var1)

        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def barplot_view(request):
    if request.method == "POST":
        var1 = request.POST['var-0']
        
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        
        values_var1 = Value.objects.filter(column=var1)

        list_values_var1 = [v.cast_value() for v in values_var1]
        
        errors=""
        #configuracion para el grafico     
        try:
            vector_var1 = robjects.FloatVector(list_values_var1)
        
        except e:
            errors = e

        name_file = "bar"+var1
        png(file=suffix_dir+name_file+ext_file)
        bar(vector_var1)
        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")

def pieplot_view(request):
    if request.method == "POST":
        var1 = request.POST['var-0']
        
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        
        values_var1 = Value.objects.filter(column=var1)

        list_values_var1 = [v.cast_value() for v in values_var1]
        
        errors=""
        #configuracion para el grafico     
        try:
            vector_var1 = robjects.FloatVector(list_values_var1)
        
        except e:
            errors = e

        name_file = "torta"+var1
        png(file=suffix_dir+name_file+ext_file)
        piechart(vector_var1)
        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")


def outqueue(request):
    
    return render(
        request,
        'outqueue.html',
        {          
            'outs':Out.objects.all().order_by('-session'),
        }
    )
