# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from models import DataSource
from forms import DataSourceForm

def index(request):
    
    form = DataSourceForm()

    if request.method == 'POST':
       form = DataSourceForm(request.POST, request.FILES)

       if form.is_valid():
            data = form.cleaned_data
            datasource = DataSource()
            datasource.name = data['name']
            datasource.attach = data['attach'].read()
            datasource.attach.content_type = data['attach'].content_type
            datasource.author = data['author']
     
            datasource.save()
       return redirect("/")

    return render(
        request,
        'index.html',
        {
            'datasource_list': DataSource.objects,
            'form': form,
        }
    )

