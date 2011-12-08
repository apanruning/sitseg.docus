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
            return redirect(workspace.get_absolute_url())

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
            return redirect(dataset.get_absolute_url())

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

            return redirect(datasource.get_absolute_url())

    return render(
        request,
        'dataset_detail.html',
        {
            'datasources_list': DataSource.objects.filter(dataset=obj),
            'dataset': obj,
            'form': form,
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
            'Densidad':'/plots/'+id+'/density',
            'Puntos':'/plots/'+id+'/stripchart',
            'Scatter':'/plots/'+id+'/scatter',
            'Scatter Matrix':'/plots/'+id+'/scattermatrix',  
            'Map':'/plots/'+id+'/map',
     }

    return render(
        request,
        'datasource_detail.html',
        {
            'datasource': instance,
            'rows':Row.objects.filter(datasource=id),
            'column_form' : ColumnForm,
            'column_forms':[ColumnForm(instance=column) for column in instance.column_set.all()],
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
    generate_documents(
        datasource=id,
        columns=request.POST.getlist('object_id')
    )
    messages.info(request, u'Se procesaron exitosamente los datos')
    if request.is_ajax:
        return render(
            request,
            'response.html',
        )
    return redirect("datasource_detail", id)

def show_data(request, id):
    qs = Row.objects.filter(datasource=id, value__isnull=False)
    sort_by = request.GET.get('sort_by')
    
    return render(
        request,
        'show_data.html',
        {
            'datasource': DataSource.objects.get(pk=id),
            'rows':qs,
        }
    )
def download_attach(request, id):

    datasource = DataSource.objects.get(id=id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response
