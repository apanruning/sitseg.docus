# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from mongoengine import connect
from bson.objectid import ObjectId
from datasources.models import DataSource, Column
from datasources.forms import DataSourceForm, ColumnFormSet, ColumnForm
from datasources.tasks import generate_documents
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
        #
        db = settings.DB
        dataset = db.data.group(
            key={instance.label:1},
            condition={'datasource_id':instance.datasource_id},
            initial={
                'count':0,
                'label': ''
            },
            reduce='''
                function(obj,prev){
                    prev.value=obj;
                    prev.count++; 
                }'''
        )
        import ipdb; ipdb.set_trace()
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
    db = settings.DB
    data = db['data'].find(datasource_id=id)
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

