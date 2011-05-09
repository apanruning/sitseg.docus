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

def download_attach(request):
    datasource_id = request.GET.get('id', '')
    datasource = DataSource.objects.get(id=datasource_id)
    attach = datasource.attach.read()
    name = datasource.slug
    
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % name

    return response

def autogenerate_columns(request):
    datasource_id = request.GET.get('id', '')
    datasource = DataSource.objects.get(id=datasource_id)    
    datasource.import_columns()
    return redirect("/")

