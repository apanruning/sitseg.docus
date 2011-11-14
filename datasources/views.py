# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from bson.objectid import ObjectId
from datasources.models import DataSource, Column, Value, Row, Workspace, DataSet
from datasources.forms import DataSourceForm, ColumnFormSet, ColumnForm, \
                                ValueForm, WorkspaceForm, DataSetForm
from datasources.tasks import generate_documents 
from datasources.utils import *
from django.db.models import Count
from django import forms

import simplejson

def workspace(request):
    ''' This function list all workspace present in database. Here is possible create a new workspace '''
    form = WorkspaceForm()
    if request.method == 'POST':

       form = WorkspaceForm(request.POST)
       if form.is_valid():
            workspace = form.save()
       return redirect("/")

    return render(
        request,
        'index.html',
        {
            'workspace_list': Workspace.objects.all(),
            'form': form,
        }
    )

def workspace_detail(request, id):
    ''' This function show the workspace's detail. It consist in a list of dataset associated with it. Here is possible create a new dataset'''
    obj = Workspace.objects.get(pk=id)
    form = DataSetForm(initial={'workspace':obj.id})
    
    if request.method == 'POST':

       form = DataSetForm(request.POST, initial={'workspace':obj.id})
       if form.is_valid():
            dataset = form.save()
       return redirect(obj.get_absolute_url())

    return render(
        request,
        'workspace_detail.html',
        {
            'dataset_list': DataSet.objects.filter(workspace=obj),
            'workspace': obj,
            'form': form,
        }
    )

def dataset_detail(request,id):
    obj = DataSet.objects.get(pk=id)
    form = DataSourceForm(initial={'dataset':obj.id})
    if request.method == 'POST':
        form = DataSourceForm(request.POST, request.FILES, initial={'dataset':obj.id})
        if form.is_valid():
            #import pdb; pdb.set_trace()
            datasource = form.save()
            datasource.import_columns()

        return redirect(obj.get_absolute_url())

    return render(
        request,
        'dataset_detail.html',
        {
            'datasources_list': DataSource.objects.filter(dataset=obj),
            'dataset': obj,
            'form': form,
        }
    )

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

    instance = get_object_or_404(DataSource, pk=id)
    plots_function = {
            'Cajas':'/plots/'+id+'/box',
            'Barras':'/plots/'+id+'/bar',
            'Torta':'/plots/'+id+'/pie',
            'Histograma':'/plots/'+id+'/hist',
            'Stripchart':'/plots/'+id+'/stripchart',
            'Densidad':'/plots/'+id+'/densityplot',
            'Puntos':'/plots/'+id+'/ptosplot',
            'Pareto':'/plots/'+id+'/paretoplot',
            'Generico':'/plots/'+id+'/genericplot',
            'ECDF':'/plots/'+id+'/ecdfplot',            
            'Scatter':'/plots/'+id+'/scatterplot',
            'Scatter Matrix':'/plots/'+id+'/scattermatrixplot',            
     }

    return render(
        request,
        'datasource.html',
        {
            'datasource': instance,
            'rows':Row.objects.filter(datasource=id),
            'column_forms':(ColumnForm(instance=column) for column in instance.column_set.all()),
            'column_labels':(v for v in ColumnForm()),
            'data_labels':(c.label for c in Column.objects.filter(datasource=id)),
            'plots':plots_function,
            
        }

    )



def delete(request, id, model=None):
    instance = get_object_or_404(model, pk=id)
    instance.delete()
    next = request.GET.get('next', '/')
    return redirect(next)

    
    
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
            'dataset': dataset.annotate(count = Count('value')), 
            'label':instance.label,
        }
    )

def import_data(request, id):
    if request.method == 'POST':
        #Aqui hay que setear los valores para cada columna que viene
        for i, v in enumerate(request.POST.getlist('object_id')):
            col = Column.objects.get(pk=v)
            col.data_type = request.POST.getlist('data_type')[i]
            if i < len(request.POST.getlist('has_geodata')):
                col.has_geodata = request.POST.getlist('has_geodata')[i]    
            else:
                col.has_geodata = False
            col.save()                            

    generate_documents(
        datasource=id,
        columns=request.POST.getlist('object_id')
    )
    messages.info(request, u'Se procesaron exitosamente los datos')
    return redirect("detail", id)

def download_attach(request, id):

    datasource = DataSource.objects.get(id=id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response
