# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from datasources.models import DataSource, Column, Value, Row, DataSet
from datasources.forms import DataSourceForm, ColumnFormSet, ColumnForm, \
                                ValueForm, DataSetForm
from datasources.tasks import generate_documents 
from django.db.models import Count
from django import forms
from django.core.files.base import ContentFile
from maap.models import MaapPoint
from datasources.forms import MaapPointForm, ExportForm
from maps import generate_shp

import simplejson

def index(request):
    initial={
        'author':request.user.id
    }
    form = DataSetForm(initial=initial)
    
    if request.method == 'POST':

       form = DataSetForm(request.POST, initial=initial)
       if form.is_valid():
            dataset = form.save()
            return redirect(dataset.get_absolute_url())

    return render(
        request,
        'index.html',
        {
            'dataset_list': DataSet.objects.all(),
            'form': form,
        }
    )

def dataset_detail(request,id):
    obj = DataSet.objects.get(pk=id)
    initial={
        'dataset':obj.id, 
        'author':request.user.id
    }
    form = DataSourceForm(initial=initial)

    if request.method == 'POST':
        form = DataSourceForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            datasource = form.save()
            datasource.import_columns()

            return redirect(obj.get_absolute_url())

    return render(
        request,
        'dataset_detail.html',
        {
            'datasources_list': DataSource.objects.filter(dataset=obj),
            'dataset': obj,
            'form': form,
        }
    )

def datasource_detail(request, id):

    instance = get_object_or_404(DataSource, pk=id)
    plots = {}

    ####### Revisar
    geo_columns = [(c.pk, c.name) for c in instance.column_set.filter(has_geodata=True, data_type="area")]
    form_export = ExportForm({'datasource':id})
    form_export.fields['column_geo'].choices = geo_columns

    if request.method == 'POST':
        if form_export.is_valid():
            areas = Value.objects.filter(column__datasource=form_export.fields['datasource_id'],column=form_export.fields['column_geo']).values("area")   
            response = HttpResponse(generate_shp(form_export.fields['name_file'], areas), mimetype='text/shp')
            response['Content-Disposition'] = 'attachment; filename=%s.shp' % form_export.fields['name_file']
            return response
    #######                    

    columns_geo = Column.objects.filter(datasource=instance,has_geodata=True)        
    
    if len(columns_geo) > 0:
        is_point = columns_geo.filter(data_type="point")
        is_area = columns_geo.filter(data_type="area")       

        if is_point:
            plots['Mapa de Puntos'] = '/plots/'+id+'/map_points'
            plots['Grafico de Densidad de Puntos'] = '/plots/'+id+'/map_point_density'

        if is_area:
            plots['Mapa de Densidad por Area'] = '/plots/'+id+'/map_density_area'
            plots['Mapa de Distribucion de una variable por area'] = '/plots/'+id+'/dist_by_area'


    plots.update({
        'Cajas':'/plots/'+id+'/box',
        'Barras':'/plots/'+id+'/bar',
        'Torta':'/plots/'+id+'/pie',
        'Histograma':'/plots/'+id+'/hist',
        'Densidad':'/plots/'+id+'/density',
        'Dispersión':'/plots/'+id+'/scatter',
        'Matriz de Dispersión':'/plots/'+id+'/scattermatrix',  
        'Gráfico de Puntos':'/plots/'+id+'/stripchart'
    })
    
    return render(
        request,
        'datasource_detail.html',
        {
            'datasource': instance,
            'rows':Row.objects.filter(datasource=id),
            'column_forms':[ColumnForm(instance=column) for column in instance.column_set.all()],
            'plots':plots,
            'form_export':form_export,
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
            'dataset': dataset.annotate(count = Count('value')), 
            'label':instance.label,
        }
    )

def import_data(request, id):
    generate_documents(
        datasource=id,
        columns=request.POST.getlist('object_id')
    )
    messages.info(request, u'Se procesaron exitosamente los datos')

    if request.is_ajax:
        return render(
            request,
            'response.html',
        )
    return redirect("datasource_detail", id)

def show_data(request, id):
    rows = Row.objects.annotate(points=Count('value__point'))
    qs = rows.filter(datasource=id, value__isnull=False)
        
    sort_by = request.GET.get('sort_by')
    if sort_by == 'right':
        qs = rows.filter(datasource=id, value__point__isnull=True, value__isnull=False)
    if sort_by == 'multiple':
        qs = rows.filter(datasource=id, value__multiple=True, value__isnull=False)
    if sort_by == 'empty':
        qs = rows.filter(datasource=id, value__map_url__isnull=True, value__isnull=False)
        

    return render(
        request,
        'show_data.html',
        {
            'datasource': DataSource.objects.get(pk=id),
            'rows':qs,
        }
    )

def delete(request, id, model=None):
    instance = get_object_or_404(model, pk=id)
    instance.delete()
    next = request.GET.get('next', '/')

    return redirect(next)

def download_attach_geom(request, id):
    datasource = DataSource.objects.get(id=id)
    rows = Row.objects.filter(datasource=datasource).order_by('-csv_index')
    value_string = ""
    separator = ';'

    #aqui se arma la primera fila del archivo 
    columns = Column.objects.filter(datasource=datasource)
    column_title=''            
    for c in columns:
        column_title += c.name.upper() + separator
        if c.has_geodata:
            if c.data_type=="point":
                column_title += "LAT" + separator
                column_title += "LNG" + separator
            else:
                column_title += "AREA" + separator
        value_string += column_title
        column_title = ''
    
    value_string = value_string[0:len(value_string)-1]
    value_string += '\n'
    
    #aqui se escriben las filas correspondientes a los datos    
    for r in range(1,len(rows)):
        row = rows[r]
        value_line = ''
        values = row.value_set.all()

        for v in values:
            print v.value    
            value_line += v.value.lower() + separator
            if v.column.has_geodata:
                if v.column.data_type=="point":
                    if v.point:
                        value_line += str(v.point.geom.x) + separator
                        value_line += str(v.point.geom.y) + separator
                elif v.column.data_type=="area":
                    if v.area:
                        value_line += str(v.area.geom) + separator
                else:
                    pass    
        value_line = value_line[0:len(value_line)-1]     
        value_string += value_line + '\n'
        value_line = ''

    attach = value_string
    value_string = ''
            
    response = HttpResponse(attach, mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % datasource.name.lower()

    return response
    
def download_attach_source(request, id):
    datasource = DataSource.objects.get(id=id)
    rows = Row.objects.filter(datasource=datasource).order_by('-csv_index')
    value_string = ""
    separator = ';'

    #aqui se arma la primera fila del archivo 
    columns = Column.objects.filter(datasource=datasource)
    column_title=''            
    for c in columns:
        column_title += c.name.upper() + separator
        if c.has_geodata:
            if c.data_type=="point":
                column_title += "LAT" + separator
                column_title += "LNG" + separator
            else:
                column_title += "AREA" + separator
        value_string += column_title
        column_title = ''
    
    value_string = value_string[0:len(value_string)-1]
    value_string += '\n'
    
    #aqui se escriben las filas correspondientes a los datos    
    for r in range(1,len(rows)):
        row = rows[r]
        value_line = ''
        values = row.value_set.all()

        for v in values:
            print v.value    
            value_line += v.value.lower() + separator

        value_line = value_line[0:len(value_line)-1]     
        value_string += value_line + '\n'
        value_line = ''

    attach = value_string
    value_string = ''
            
    response = HttpResponse(attach, mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % datasource.name.lower()

    return response

