# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from bson.objectid import ObjectId
from datasources.models import DataSource, Column, Value, Row
from datasources.forms import DataSourceForm, ColumnFormSet, ColumnForm, ValueForm
from datasources.tasks import generate_documents
from datasources.utils import *

import simplejson

def datasource(request):

    form = DataSourceForm()
    column_form = ColumnFormSet()
    if request.method == 'POST':

       form = DataSourceForm(request.POST, request.FILES)

       if form.is_valid():
            data = form.cleaned_data
            datasource = form.save()
            datasource.import_columns()                
       
       return redirect("/")

    return render(
        request,
        'index.html',
        {
            'datasource_list': DataSource.objects.order_by('-created'),
            'form': form,
            'column_form': column_form
        }
    )

def datasource_detail(request, id):

    column_form = ColumnForm()
    instance = get_object_or_404(DataSource, pk=id)
    columns = (ColumnForm(instance=column) for column in instance.column_set.all())
    return render(
        request,
        'datasource.html',
        {
            'datasource': instance,
            'columns': columns,
            'column_form':column_form,
        }
    )
    
    
def column_detail(request, id):
    instance = get_object_or_404(Column, pk=id)
    if request.method == "POST":
        column_form = ColumnForm(request.POST, instance=instance )
        if column_form.is_valid():
            instance = column_form.save()

        return render(
            request,
            'column_obj.html',
            {
                'column':column_form,
            }
        )

    dataset = Value.objects.filter(column=instance)

    return render(
        request,
        'column.html',
        {
            'column':instance,
            'dataset': dataset,
            'label':instance.label,
        }
    )

def import_data(request, id):
    columns = []
    if request.method == 'POST':
        columns = request.POST.getlist('object_id')
    import pdb
    pdb.set_trace()
    generate_documents.delay(
        datasource=id,
        columns=columns
    )
    messages.info(request, u'Estamos procesando los datos')
    return redirect("detail", id)

def show_data(request, id):
    values = Value.objects.filter(column__datasource = id)
    values_form = (ValueForm(instance=value) for value in values)

    datasource = DataSource.objects.get(id=id)
    return render(
        request,
        'data.html',
        {
            'datasource': datasource,
            'dataset': values_form,
        }
    )


def download_attach(request, id):

    datasource = DataSource.objects.get(id=id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response

def stats(request,id):
    instance = Column.objects.get(pk=int(id))
    values = Value.objects.filter(column=instance.id)
    
    if not instance.has_geodata:
        #La columna no es geoposicionada        
        #aca deberian mostrarse n posibles estadisticas para los datos de esa columna
        #Se devuelve un diccionario en el contexto
        import pdb
        pdb.set_trace()
        
        if instance.data_type=="int" or instance.data_type=="float":
            dist = Distribucion(len(lista_values))
            dist.elementos = values
            res = {
                'casos':dist.n,
                'min':dist.minimo(),
                'max':dist.maximo(),
                'rango':dist.rango(),
                'media':dist.media(),
                'mediana':dist.mediana(),
                'varianza':dist.varianza(),
                'desv_estandar':dist.desviacion(),
            }
            
            
        else:
            res = values.order_by('value')
    else:
        #La columna es geoposicionada
        #aca deberian mostrarse m posibles estadisticas para los datos de esa columna
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

