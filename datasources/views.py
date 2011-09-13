# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from bson.objectid import ObjectId
from datasources.models import DataSource, Column
from datasources.forms import DataSourceForm, ColumnFormSet, ColumnForm
from datasources.tasks import generate_documents
from settings import DB

import simplejson

def datasource(request):

    form = DataSourceForm()
    column_form = ColumnFormSet()
    if request.method == 'POST':
        form = DataSourceForm(request.POST, request.FILES)
        column_form = ColumnFormSet(request.POST)

        if form.is_valid():
            datasource = form.save()
            datasource.import_columns()
        else:
            return redirect("/")

        return redirect('detail', datasource.pk)

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
    columns = [ColumnForm(instance=column) for column in instance.column_set.all()]
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
    try:
        dataset = DB.dattum.group(
            key={instance.label:1},
            condition={'datasource_id':instance.datasource_id},
            initial={
                'count':0,
                'value': '',
                'point': []
            },
            reduce='''
                function(obj,prev){
                    label = '%s'
                    prev.value = obj[label]['value'];
                    prev.point = obj[label]['point'];
                    prev.count++; 
                }
            ''' % instance.label)
        
    except Exception, e:
        messages.error(request, e)
        return redirect('detail', instance.datasource_id)
    else:
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

    generate_documents.delay(
        datasource=id,
        columns=columns
    )
    messages.info(request, u'Estamos procesando los datos')
    return redirect("detail", id)

def show_data(request, id):
    datasource = DataSource.objects.get(id=id)
    
    data = DB.dattum.find({'datasource_id':datasource.pk})
    sort_by = request.GET.get('sort_by')

    if sort_by == 'empty':
        data = data.filter(columns__point=None, columns__map_multiple__ne=True)
    if sort_by == 'multiple':
        data = data.filter(columns__map_multiple=True)
    if sort_by == 'ok':
        data = data.filter(columns__point__ne=None, columns__map_multiple__ne=True)
    
    return render(
        request,
        'data.html',
        {
            'datasource': datasource,
            'dataset': data,
        }
    )


def geometry_append(request, datasource_id, id):
    db = settings.DB
    # This create the collection if not exists previously
    data_collection = db['data']
    
    column_id = request.get("column_id", "")
    maapmodel_id = request.get("maapmodel_id", "")
    
    oid = ObjectId(id)
    document_args = dict()
    document_args[column_id+"_geom_id"] = maapmodel_id
    
    data_collection.find_one({"_id": oid}).update(document_args)
    
    return redirect('detail', id)


def download_attach(request, id):

    datasource = DataSource.objects.get(id=id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response

