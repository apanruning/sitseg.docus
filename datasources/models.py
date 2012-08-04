# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from maap.models import MaapPoint, MaapArea
from dateutil.parser import parse as date_parser
from django.template.defaultfilters import slugify
from django import forms
from datetime import datetime
from celery.task import task
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps
from django.contrib.gis.geos import Point
from unicodedata import normalize
from django.core.cache import cache
from hashlib import sha1
from django.template.defaultfilters import slugify
from djangoosm.utils.words import normalize_street_name
from re import match
from interface_r import gooJSON
import xlrd

class Annotation(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=50)
    datasource = models.ForeignKey('DataSource')

class Column(models.Model):
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    datasource = models.ForeignKey('DataSource', editable=False)
    is_available = models.BooleanField(default=True,)
    csv_index = models.IntegerField(editable=False)
    data_type = models.CharField(max_length=50)
    has_geodata = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['csv_index',]

    def save(self):
        self.datasource.is_dirty = True
        self.datasource.save()
        if self.data_type in ['point', 'area']:
            self.has_geodata = True

        return super(Column,self).save()
        
class DataSet(models.Model):
    name = models.CharField("Nombre", max_length=50)
    slug = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    author = models.ForeignKey('auth.User')

    @models.permalink
    def get_absolute_url(self):
        return ('dataset_detail',[self.pk])

    def save(self):
        self.slug = slugify(self.name)
        return super(DataSet, self).save()

    def __str__(self):
        return self.name

class DataSource(models.Model):
    name = models.CharField("Nombre",max_length=50)
    slug = models.CharField(max_length=50,editable=False)
    attach = models.FileField("Archivo", upload_to='docs/')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    author = models.ForeignKey('auth.User')
    is_dirty = models.BooleanField(default=True, editable=False)
    dataset = models.ForeignKey('DataSet')
    geopositionated = models.BooleanField(default=False, editable=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ('datasource_detail',[self.pk])

    def __unicode__(self):
        return '%s-%d' %(slugify(self.name), self.id)

    def save(self):
        if self.slug is None:
            slug = slugify(self.name)
            new_slug = slug
            c = 1
            while True:
                try:
                    DataSource.objects.get(slug=new_slug)
                except DataSource.DoesNotExist:
                    break
                else:
                    c += 1
                    new_slug = '%s-%s' % (slug, c)
                    
            self.slug = new_slug

        return super(DataSource, self).save()

    def import_columns(self):
        sh = self.open_source()

        Column.objects.filter(datasource=self).delete()
        
        for colnum in range(0,sh.ncols):
            row = sh.col_values(colnum)           
            new_column = Column()
            new_column.name = row[0]
            new_column.created = datetime.now()
            new_column.label = slugify(new_column.name)
            new_column.csv_index = colnum
            new_column.datasource = self 
            new_column.is_available = True
            new_column.save()

    def get_column_names(self):
        columns_name = Column.objects.filter(datasource=self)
        return columns_name

    def xls_to_orm(self, columns=None):
        
        row_excluded = []
        
        file = self.attach

        errors = []

        #se seleccionan las columnas segun la decision del usuario. En caso de no elegir al menos una el sistema importa la totalidad de las columnas    
        if columns:
            columns = self.column_set.filter(pk__in=columns)
        else:
            columns = self.column_set.all()

        #Se borran los viejos elementos del datasource
        self.delete_old_values()
        src = self.open_source()
        
        for column in columns:
            #Para cada columna que el usuario haya seleccionado para importar, se recorren todos sus valores creando objetos del tipo ValueX donde X es el tipo del valor que se esta recorriendo
            
            col_tp = src.col_types(column.csv_index,start_rowx=1)

            for i, val in enumerate(src.col_values(column.csv_index,start_rowx=1)):
                #Para cada valor asociado a la columna seleccionada (column) se crea una instancia del tipo Valor               
                if col_tp[i] == 1 and column.data_type=='point':
                    value = ValuePoint()
                elif col_tp[i] == 1 and column.data_type=='area':
                    value = ValueArea()
                elif col_tp[i] == 1 and column.data_type!='area' and column.data_type!='point':
                    value = ValueText()
                elif col_tp[i] == 2:
                    value = ValueFloat()
                elif col_tp[i] == 3:
                    value = ValueDate()
                elif col_tp[i] == 4:
                    value = ValueBool()
        
                value.value = val
                value.data_type = col_tp[i]
                value.column = column

                #Se crea una nueva instancia de fila
                row_obj = Row(datasource=self,csv_index=i+1)
                row_obj.save()

                value.row = row_obj

                value.save()

                search_term = slugify(value.value)
                self.geopositionated = False
                #SI LOS DATOS SON GEOPOSICIONADOS
                if column.data_type == 'point':
                    #gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
                    self.geopositionated = True
                        
                    #se debe hacer primero una consulta a la base local
                    results = MaapPoint.objects.filter(slug=search_term)

                    

                    if len(results) >= 1:
                        #En este caso quiere decir que la consulta a la base local fue exitosa

                        for point in results:
                            value.point = point
                            value.map_url = point.static_url
                            value.save()
    
                    if len(results) < 1: 
                        #Este caso quiere decir que la consulta a la base local no fue exitosa y por lo tanto se procede a buscarlo via web. Aca se debe controlar solo el caso que sea unico. Ahora esta asi porque hay muchos MaapPoint iguales

                        #results = gmaps.local_search('%s, cordoba, argentina' %value.value )['responseData']['results']
                        #for result in results:
                        #latlng = [float(result.get('lng')), float(result.get('lat'))]

                        #    point =  MaapPoint(
                        #        geom=Point(latlng).wkt,
                        #        name=value.value,
                        #    )
                            
                        #    point.static_url = result.get('staticMapUrl', None)
                        #    point.save()
                        #    value.point = point
                        #    value.map_url = point.static_url
                        #    value.save()
                        results = gooJSON.goomap(gooJSON.gooadd(address=[value.get_value(),'CORDOBA','AR']), settings.GOOGLEMAPS_API_KEY)
                        
                        print results

                
                #SI LOS DATOS SON GEOPOSICIONADOS                        
                if column.data_type == 'area':
                    self.geopositionated = True
                    barrio = MaapArea.objects.filter(slug=search_term) 

                    if len(barrio) == 1:
                        value.area = barrio[0]
                        value.save()

        if len(errors) == 0:
            self.is_dirty = False 
            self.save() 
            
            if self.geopositionated:
                values_geo = Value.objects.filter(column__datasource=self,column__has_geodata=True)
                for t in values_geo:
                    qs = Value.objects.filter(column__datasource=self,column__has_geodata=False,row=t.row)        
                    for u in qs:
                        u.area = t.area
                        u.save()

        print errors
        return self.get_absolute_url()

    def delete_old_values(self):
        #se borran los valores viejos que correspondan a ese datasource     
        Value.objects.filter(column__datasource=self.id).delete()
        Value.objects.filter(row__datasource=self.id).delete()
        ValueInt.objects.filter(column__datasource=self.id).delete()
        ValueInt.objects.filter(row__datasource=self.id).delete()
        ValueFloat.objects.filter(column__datasource=self.id).delete()
        ValueFloat.objects.filter(row__datasource=self.id).delete()
        ValueText.objects.filter(column__datasource=self.id).delete()
        ValueText.objects.filter(row__datasource=self.id).delete()
        ValueDate.objects.filter(column__datasource=self.id).delete()
        ValueDate.objects.filter(row__datasource=self.id).delete()
        ValuePoint.objects.filter(column__datasource=self.id).delete()
        ValuePoint.objects.filter(row__datasource=self.id).delete()
        ValueArea.objects.filter(column__datasource=self.id).delete()
        ValueArea.objects.filter(row__datasource=self.id).delete()

        #se borran las filas que correspondan a ese datasource
        Row.objects.filter(datasource=self).delete()
        

    def open_source(self):
        #se abre la planilla
        wb = xlrd.open_workbook(file_contents=self.attach.read()    )
        sh = wb.sheet_by_index(0)
        return sh

    def xls_to_list_of_list(self):
        sh = self.open_source()
        data = []

        for rownum in range(1,sh.nrows):
            data.append(sh.row_values(rownum))
        return data

    def xls_to_list_of_model_values(self):
        rows = self.row_set.all().order_by('csv_index')        
        results = []
        for r in rows:
            results.append(Value.objects.filter(row=r))

        return results

class Row(models.Model):
    datasource = models.ForeignKey(DataSource)    
    csv_index = models.IntegerField()

def search(search_list, i, field, value, res):
    if i < len(search_list):
        if search_list[i][field] == value:    
            res.append(search_list[i])
            return search(search_list, i+1, field, value, res)        
        else:
            return search(search_list, i+1, field, value, res)                    
    else:
        return res

def get_all_values(datasource=None):
    result = list()
    if not datasource:
        valueint = list(ValueInt.objects.values())
        valuetext = list(ValueText.objects.values())
        valuedate = list(ValueDate.objects.values())
        valuefloat = list(ValueFloat.objects.values())
        valuebool = list(ValueBool.objects.values())
        valuepoint = list(ValuePoint.objects.values())
        valuearea = list(ValueArea.objects.values())
        result += valueint+valuetext+valuedate+valuefloat+valuebool+valuepoint+valuearea
    else:
        valueint = list(ValueInt.objects.filter(datasource=datasource).values())
        valuetext = list(ValueText.objects.filter(datasource=datasource).values())
        valuedate = list(ValueDate.objects.filter(datasource=datasource).values())
        valuefloat = list(ValueFloat.objects.filter(datasource=datasource).values())
        valuebool = list(ValueBool.objects.filter(datasource=datasource).values())
        valuepoint = list(ValuePoint.objects.filter(datasource=datasource).values())
        valuearea = list(ValueArea.objects.filter(datasource=datasource).values())
        result += valueint+valuetext+valuedate+valuefloat+valuebool+valuepoint+valuearea

    return result

class Value(models.Model):
    column = models.ForeignKey(Column)
    data_type = models.IntegerField()
    row = models.ForeignKey(Row)

    
    def get_value(self):
        value = ''
        for i in ('value_point', 'value_area', 'value_text', 'value_int', 'value_date', 'value_bool'):
            try:
                value = getattr(self, i)
            except AttributeError:
                pass
        return value

class ValueInt(Value):
    value = models.IntegerField()    

class ValueText(Value):
    value = models.TextField()
    area = models.ForeignKey(MaapArea, null=True, blank=True)
    point = models.ForeignKey(MaapPoint, null=True, blank=True)

class ValueFloat(Value):
    value = models.FloatField()

class ValueBool(Value):
    value = models.BooleanField()

class ValueDate(Value):
    value = models.DateField()

class ValuePoint(Value):
    value = models.TextField()
    point = models.ForeignKey(MaapPoint, null=True, blank=True)
    map_url = models.URLField(null=True, blank=True)

class ValueArea(Value):
    value = models.TextField()
    area = models.ForeignKey(MaapArea, null=True, blank=True)
    map_url = models.URLField(null=True, blank=True)

class Out(models.Model):
    text = models.TextField(blank=True)
    session = models.DateTimeField(default=datetime.now(),editable=False) 
    img = models.CharField(max_length=50)
    errors = models.TextField(blank=True)

__all__ = ['DataSource', 'Column', 'Annotation','DataSet','ValueInt','ValueFloat','ValueText','ValueBool']
