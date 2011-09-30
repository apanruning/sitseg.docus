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

    generate_documents(
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

