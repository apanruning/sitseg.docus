# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import DataSource, Column
from forms import DataSourceForm, ColumnFormSet
from mongoengine.django.auth import User

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
                import ipdb; ipdb.set_trace()
                datasource.columns.append(column.instance)
        
        datasource.save()
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

