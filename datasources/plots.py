# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

def scatter_plot(request, datasource_id):
    datasource = DataSource.objects.get(pk=datasource_id)
    db = settings.DB
    columns = datasource.column_set.all()
    context = {
        'datasource': datasource,
        'columns': columns,            
    }

    if request.method == 'POST':

        column1 = request.POST.get('column1', None)
        column2 = request.POST.get('column2', None)
        
        data = db.data.find(
            {
                'datasource_id': int(datasource_id)}, 
                {column1:1,column2:1
            }
        )
        datalist = [{
                column1:item[column1],
                column2:item[column2],                
            } for item in data]
        
        context['scatterdata'] = datalist
        context['labels'] = [column1, column2]
    return render(
        request,
        'scatter_form.html',
        context,
    )    

