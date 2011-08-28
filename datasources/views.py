# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from models import DataSource, Column
from forms import DataSourceForm, ColumnFormSet, ColumnForm
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from mongoengine import connect
from bson.objectid import ObjectId
from django.conf import settings
from django.contrib import messages

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
        'detail.html',
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
    if instance.is_available:
        db = settings.DB
        dataset = db.data.group(
            key={instance.label:1},
            condition={'datasource_id':instance.datasource_id},
            initial={
                'count':0,
                'value': ''
            },
            reduce='function(obj,prev){prev.value=obj.%s["value"];prev.count++; }' % instance.label
        )
        return render(
            request,
            'column.html',
            {
                'column':instance,
                'dataset': dataset,
                'label':instance.label,
                
            }
        )
    else:
        messages.error(request, u'La columna no está disponible')
        return redirect('/')


def import_data(request, id):
    datasource = DataSource.objects.get(id=id)

    if request.method == 'POST':

        import_result = datasource.generate_documents(
            columns=request.POST.getlist('object_id')
            )

    else:
        datasource.generate_documents()
    return redirect("detail", id)

def show_data(request, id):
    datasource = DataSource.objects.get(id=id)    
    data = datasource.find()
    return render(
        request,
        'data.html',
        {
            'datasource': datasource,
            'data': data,
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

