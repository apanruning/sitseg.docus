# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from datasources.models import Column, Value, DataSource, Out
from datasources.interface_r import *
from django import forms
from maap.models import MaapArea, MaapPoint
from maap.layers import Layer
from django.db.models import Count
import os

class CommentFormTwo(forms.Form):
    column_geo = forms.ChoiceField(label='Variable')
    column_value = forms.ChoiceField(label='Variable')
    datasource = forms.CharField(widget=forms.HiddenInput)

class CommentForm(forms.Form):
    column_geo = forms.ChoiceField(label='Variable')
    datasource = forms.CharField(widget=forms.HiddenInput)

def map_area_r_form(request, id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True, data_type="area")]
    form = CommentForm({'datasource':id})
    form.fields['column_geo'].choices = geo_columns
    description = u"Este gráfico permite ver los datos agrupados por área"

    return render(
        request,
        'map.html', 
        {
            'datasource': datasource,
            'form':form,
            'action':'/graph/map_area_r_plot',
            'description':description,
        }
    )

def density_by_area_form(request, id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True, data_type="area")]
    form = CommentForm({'datasource':id})
    form.fields['column_geo'].choices = geo_columns

    return render(
        request,
        'map.html', 
        {
            'datasource': datasource,
            'form':form,
            'action':'/graph/density_by_area_plot',
        }
    )

def generate_shp(query, name_file):
    
    shp_cmd = settings.PATH_TO_PGSQL2SHP+"pgsql2shp -f " + settings.SHP_UPLOAD_DIR + name_file + ' -h localhost -u postgres ' + settings.DATABASES['default']['NAME']     
    sql_query = " select * from maap_maaparea where maapmodel_ptr_id in "
    id_areas = []
    for area in query:
        if area['area']:
            id_areas.append(area['area'])            
    os.system(shp_cmd + " '" + sql_query + str(tuple(id_areas))+"'")
    shp_file = open(settings.SHP_UPLOAD_DIR+name_file, "rb").read()

    return shp_file

    
def map_area_r_view(request):
    datasource_id = request.POST.get('datasource')
    column_geo = request.POST.get('column_geo')
    
    datasource = DataSource.objects.get(pk=datasource_id)

    areas = Value.objects.filter(column__datasource=datasource_id,column=column_geo).values("area").annotate(Count('area')).order_by()

    shp_name = str(int(datasource_id)+int(column_geo))

    min_val = 0
    max_val = 1023
    
    polys = []
                
    suffix_dir = "media/graphics/"
    ext_file = ".png"

    main = "Grafico de Densidad Por Puntos de %s"
    xlab = "Latitud"
    ylab = "Longitud"

    png(file=suffix_dir+shp_name+ext_file)
    generate_shp(areas,shp_name+'.shp')
    shp_file = pbsmapping.importShapefile(settings.SHP_UPLOAD_DIR+shp_name)
    pbsmapping.plotPolys(shp_file)
    off()
    out = Out()
    out.img = str(shp_name+ext_file)
    out.save()

    return redirect("/outqueue")

def density_by_area_view(request):
    datasource_id = request.POST.get('datasource')
    column_geo = request.POST.get('column_geo')
    
    datasource = DataSource.objects.get(pk=datasource_id)
    flag = Column.objects.get(pk=column_geo).data_type

    areas = Value.objects.filter(column__datasource=datasource_id,column=column_geo).values("area").annotate(Count('area')).order_by()

    min_val = min(float(r['area_count']) for r in areas)
    max_val = max(float(r['area_count']) for r in areas)

    layer = Layer()
    for area in areas:
        if flag == 'area':

            if area['area']:
                maap_area = MaapArea.objects.get(pk=area['area'])
                area['geo'] = maap_area.to_geo_element()
                color = int((area['area__count']-min_val)*256/(max_val-min_val))-1
                area['geo'].color = "#%x0000" % color
                area['geo'].name = "%s (%d)" %(maap_area.name, area['area__count']) 
                layer.elements.append(area['geo'])

    return render(
        request,
        'map_area_point.html',
        {
            'objects': areas,
            'datasource': datasource,
            'json_layer': layer.json, 
            'column_geo':Column.objects.get(pk=column_geo).name
        }
    )

def map_points_form(request, id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True,data_type="point")]
    form = CommentForm({'datasource':id})
    form.fields['column_geo'].choices = geo_columns
    description = u"Este gráfico se utiliza para ver como se distribuyen los puntos en una zona determinada. Permite tener una idea aproximada de donde se concentran (espacialmente) los datos"

    return render(
        request,
        'map.html', 
        {
            'datasource': datasource,
            'form':form,
            'action':'/graph/map_points_plot',
            'description': description,
        }
    )
    
def map_points_view(request):
    datasource_id = request.POST.get('datasource')
    column_geo = request.POST.get('column_geo')
    
    datasource = DataSource.objects.get(pk=datasource_id)
    
    points = Value.objects.filter(column=column_geo)

    layer = Layer()
        
    for p in points:
        maap_point = p.valuepoint.point                   
        r = {}
        r['geo'] = maap_point.to_geo_element()
        r['geo'].name = "%s" %(maap_point.name) 
        r['geo'].icon = "/media/icons/favicon.jpg"
        
        layer.elements.append(r['geo'])
        
    return render(
        request,
        'map_area_point.html',
        {
            'objects': [(str(p.valuepoint.point.geom.x),str(p.valuepoint.point.geom.y)) for p in points],
            'datasource': datasource,
            'json_layer': layer.json, 
            'column_geo':Column.objects.get(pk=column_geo).name,
            'max':len(points),
        }
    )


def dist_by_area_form(request,id):
    datasource = DataSource.objects.get(pk=id)
    
    # Create form on the fly. Problem? 
    columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=False)]
    geo_columns = [(c.pk, c.name) for c in datasource.column_set.filter(has_geodata=True,data_type="area")]
    form = CommentFormTwo({'datasource':id})
    form.fields['column_value'].choices = columns
    form.fields['column_geo'].choices = geo_columns
    description = u"Este gráfico permite ver cómo se distribuye una variable cuantitativa sobre las áreas"
    
    return render(
        request,
        'map.html',
        {
            'datasource': datasource,
            'form':form,
            'action':'/graph/dist_by_area_plot',
            'description':description,
        }
    )

def dist_by_area_view(request):
    datasource_id = request.POST.get('datasource')
    column_geo = request.POST.get('column_geo')
    column_value = request.POST.get('column_value')
    datasource = DataSource.objects.get(pk=datasource_id)
    
    # Problem? :D
    rows = [(
                r.value_set.get(column__pk=column_geo).area, 
                r.value_set.get(column__pk=column_value).value
            ) 
            for r in datasource.row_set.all() if len(r.value_set.all())!=0]

    #Assume that column has only numbers
    areas = {}
    for geo, value in rows:
        if geo:
            if geo.pk in areas.keys():
                areas[geo.pk]['total'] += float(value)
            else:
                areas[geo.pk] = {
                    'total':float(value),
                    'geo': geo.to_geo_element(),
                }

    min_val = min(r['total'] for r in areas.itervalues())
    max_val = max(r['total'] for r in areas.itervalues())

    layer = Layer()
    for area in areas.itervalues():
        color = int((area['total']-min_val)*256/(max_val-min_val))-1
        area['geo'].color = "#%x0000" % color
        area['geo'].name = "%s (%d)" %(area['geo'].name, area['total']  ) 
        layer.elements.append(area['geo'])
                   
    return render(
        request,
        'map_area_point.html',
        {
            'objects': areas,
            'datasource': datasource,
            'json_layer': layer.json, 
            'column_geo':column_geo,
            'column_value':column_value,
        }
    )

def zonemap():
    pass

def pointmap():
    pass

