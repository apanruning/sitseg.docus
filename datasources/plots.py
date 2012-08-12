# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource, Out
from datasources.interface_r import *
from django import forms

class CommentForm(forms.Form):
    column_geo = forms.ChoiceField(label='Variable')
    datasource = forms.CharField(widget=forms.HiddenInput)

def listDataSourcesDataset(datasource):
    
    return datasource.dataset.datasource_set.all()

def histplot(request,id):
    datasource = DataSource.objects.get(pk=id)
   
    options = {
                'labels':['Seleccione Variable'],
                'action':'/graph/histogram',
    }

    description = u"Este gráfico permite construir histogramas a partir de una variable. Permite ver rapidamente la densidad de la misma"

    return render(
        request,
        'graphic.html',
        {          
            'datasources':listDataSourceDataset(datasource),
            'options':options,
            'dataset':datasource.dataset,
            'description':description,
        }
    )

def box(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []

    for ds in dataset.datasource_set.all():
        datasources.append(ds)
   
    options = {
                'labels':['Seleccione Variable'],
                'action':'/graph/boxplot',
    }

    description = u"El histograma de un conjunto de datos es un gráfico de barras que representan las frecuencias con que aparecen las mediciones agrupadas por variables"

    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
            'description':description,
        }
    )

def scatter(request,id):
    datasource = DataSource.objects.get(pk=id)
    dataset = datasource.dataset
    datasources = []
    for ds in dataset.datasource_set.all():
        datasources.append(ds)
    
    options = {
        'labels':['Seleccione Variable','Seleccione Variable'],
        'action':'/graph/scatterplot',
    }

    description = u"Este gráfico permite ver rápidamente si dos variables están relacionadas entre si"
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
            'description':description,
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
    
    options = {
        'labels':['Seleccione Variable'],
        'action':'/graph/pieplot',
    }

    description = u"Este grafico permite ver la distribución de una variable pero de manera porcentual"

    return render(
        request,
        'graphic.html',
        {          
            'datasources':listDataSourcesDataset(datasource),
            'options':options,
            'dataset':datasource.dataset,
            'description':description,
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
    description = u"Este gráfico permite observar la densidad de una variable"
    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
            'description':description,
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

    description = u"Este gráfico permite observar la cantidad de ocurrencias para cada valor de una variable"

    return render(
        request,
        'graphic.html',
        {          
            'datasources':datasources,
            'options':options,
            'dataset':dataset,
            'description':description,
        }
    )

def map_point_density_form(request,id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True,data_type="point")]
    form = CommentForm({'datasource':id})
    form.fields['column_geo'].choices = geo_columns
    description = u"Este gráfico se utiliza para ver como se concentran los datos espacialmente. Es una grafico de dispersión. "

    return render(
        request,
        'map.html',
        {          
            'datasource': datasource,
            'form':form,
            'action':'/graph/map_point_density',
        }
    )

def map_point_density_view(request):
    if request.method == "POST":
        var1 = request.POST['column_geo']
        
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        
        values_var1 = Value.objects.filter(column=var1)

        point_values_lat = [p.point.geom.x for p in values_var1 if p.point]
        point_values_lng = [p.point.geom.y for p in values_var1 if p.point]
        
        errors=""
        vector_var1 = robjects.FloatVector(point_values_lat)
        vector_var2 = robjects.FloatVector(point_values_lng)
      
        main = "Grafico de Densidad Por Puntos de %s" %(Column.objects.get(pk=int(var1)).name)
        xlab = "Latitud"
        ylab = "Longitud"

        name_file = "density_point"+var1
        png(file=suffix_dir+name_file+ext_file)
        scatterplot(vector_var1,vector_var2,main=main,xlab=xlab,ylab=ylab)
        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return redirect("/outqueue")


#Funciones que graficar (se conectan directamente con R)
def histogram_view(request):
    if request.method == "POST":
        var = request.POST['var-0']
        
        #configuracion para tipo de archivo donde se guarda el grafico y nombre del mismo
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        name_file = "histograma"+var
        png(file=suffix_dir+name_file+ext_file)
        errors = ''
        
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

        try:
            hist(vector,col=col,border=border,main=main,xlab=xlab,ylab=ylab)
            off()
        except UnboundLocalError:
            errors += ""

        #Guardo el resultado y lo muestro en la cola de salida
        out = Out()
        out.img = str(name_file+ext_file)
        out.errors = errors
        out.text = main
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
        main="Grafico de Caja para %s" %(Column.objects.get(pk=var).name)
        xlab="Valores"


        boxplot(vector,main=main,xlab=xlab)
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
        jitter=0.2 
        offset=1/3
        vertical=False
        main="Grafico de Puntos para %s" %(Column.objects.get(pk=var).name)
        ylab="Valores"
        xlab=""
        pch=1
        col=par("fg")
        cex=par("cex")

        strip(vector,method="jitter",jitter=jitter,offset=offset,vertical=vertical,main=main,xlab=xlab,pch=pch,col=col,cex=cex)
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
        vector_var1 = robjects.FloatVector(list_values_var1)
        vector_var2 = robjects.FloatVector(list_values_var2)
      
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

        vector_var1 = robjects.FloatVector(list_values_var1)
        vector_var2 = robjects.FloatVector(list_values_var2)
     
        main="Grafico de Dispersion para %s" %(Column.objects.get(pk=var1).name+'-'+Column.objects.get(pk=var2).name)
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

        #configuracion para tipo de archivo donde se guarda el grafico y nombre del mismo
        suffix_dir = "media/graphics/"
        ext_file = ".png"
        name_file = "density"+var1
        png(file=suffix_dir+name_file+ext_file)
        
        values_var1 = Value.objects.filter(column=var1)

        list_values_var1 = [v.cast_value() for v in values_var1]
        
        errors=""

        #configuracion para el grafico     
        vector = robjects.FloatVector(list_values_var1)
        
        main="Grafico de Densidad para"+Column.objects.get(pk=var1).name
        xlab="Valores"

        densityplot(vector,main=main,xlab=xlab)
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

        list_values_var1 = [v.get_value() for v in values_var1]
        
        errors=""

        #configuracion para el grafico     
        vector_var1 = robjects.StrVector(list_values_var1)
       
        name_file = "torta"+var1
        png(file=suffix_dir+name_file+ext_file)
        piechart(vector_var1)
        off()
        out = Out()
        out.img = str(name_file+ext_file)
        out.save()

        return outqueue(request)

def outqueue(request):
    return render(
        request,
        'outqueue.html',
        {          
            'outs':Out.objects.all().order_by('-session'),
            }
    )
