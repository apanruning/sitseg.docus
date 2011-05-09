# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import DataSource, Column
from forms import DataSourceForm, ColumnFormSet
from mongoengine.django.auth import User
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

def index(request):
    
    form = DataSourceForm()
    column_form = ColumnFormSet()
    if request.method == 'POST':
        form = DataSourceForm(request.POST, request.FILES)
        column_form = ColumnFormSet(request.POST)
        if form.is_valid():
            datasource = form.save()
            for column in column_form.forms:
                if column.is_valid():
                    column_instance = Column(**column.cleaned_data)
                    datasource.columns.append(column.instance)
                    datasource.save()
        else:
            import ipdb; ipdb.set_trace()  
      
        
        return redirect("/")


    return render(
        request,
        'index.html',
        {
            'datasource_list': DataSource.objects.order_by('created'),
            'form': form,
            'column_form': column_form
        }
    )

def detail(request, id):
    datasource = DataSource.objects.get(id=id)
    return render(
        request,
        'detail.html',
        {
            'datasource': datasource,
        }
    )
    

def download_attach(request, id):

    datasource = DataSource.objects.get(id=id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response

def autogenerate_columns(request, id):
    datasource = DataSource.objects.get(id=id)    
    datasource.import_columns()
    return redirect("/")

def import_data(request, id):
    datasource = DataSource.objects.get(id=id)    
    datasource.generate_documents()
    return redirect("/")


def data_formatted(data, columns_dict):
    """ takes a plain data and columns info and generate a list of labeled values"""
    for document in data:
        doc_formatted = []
        for key, column in columns_dict.iteritems():
        
            doc_formatted.append(dict(
                label = column['name'],
                key = key,
                value = document[key],
                field_type = column['data_type']
            ))
        yield doc_formatted

def show_data(request, id):
    datasource = DataSource.objects.get(id=id)    
    data = datasource.find()[:10]
    #import ipdb; ipdb.set_trace()
    return render(
        request,
        'data.html',
        {
            'datasource': datasource,
            'data': data_formatted(data, datasource.columns_dict)
        }
    )


