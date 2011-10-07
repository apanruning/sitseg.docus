# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps
from datasources.models import DataSource, Value, Row
from django.contrib.gis.geos import Point
from datasources.models import DataSource, Value
from maap.models import MaapPoint


@task
def generate_documents(datasource, columns=None):

    gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
    datasource = DataSource.objects.get(id=datasource)
    region = settings.DEFAULT_REGION
    csv_attach = reader(StringIO(datasource.attach.read()))
    first_column = csv_attach.next() # skip the title column.
    errors = []
    
    if columns:
        columns = datasource.column_set.filter(pk__in=columns)
    else:
        columns = datasource.column_set.all()
        
    for i, row in enumerate(csv_attach):
        row_obj = Row()
        row_obj.datasource = datasource
        row_obj.csv_index = i
        row_obj.save()
        
        for column in columns:
            value.data_type = column.data_type
            if column.data_type == 'str':
                value = ValueText()
                value.value = row[column.csv_index]
            elif column.data_type == 'int':
                value = ValueInt()
                value.value = int(row[column.csv_index])
            elif column.data_type == 'float':
                value = ValueFloat()
                value.value = float(row[column.csv_index])
            elif column.data_type == 'bool':
                value = ValueBool()
                value.value = bool(row[column.csv_index])   
            elif column.data_type == 'date':
                import time, datetime
                time_format = "%d-%m-%Y"
                value = ValueDate()
                value.value = datetime.datetime.fromtimestamp(time.mktime(time.strptime(row[column.csv_index], time_format)))
            elif column.data_type == 'point':
                latlng = gmaps.address_to_latlng('%s, cordoba, argentina' %value.value )
                try:
                    point =  MaapPoint(
                        geom=Point(latlng).wkt,
                        name=value.value,
                    )
                    point.save()            
                except Exception, e:
                    errors.append(e)
                else:
                    value.value = row[column.csv_index]
                    value.point = point
            
            value.row = row_obj
            value.column = column
            
            value.save()
            
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 


    print errors
