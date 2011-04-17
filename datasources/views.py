# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import DataSource
from forms import DataSourceForm
def index(request):
    return render(
        request,
        'index.html',
        {'datasource_list': DataSource.objects}
    )

def create(request):

    if request.method == 'POST':
       form = DataSourceForm(request.POST)
       
       if form.is_valid():
           form.save()
       return HttpResponseRedirect("/")

    else:
        form = DataSourceForm()
        
    return render(
        request,
        'datasource_create.html',
        {'form': form}
    )
