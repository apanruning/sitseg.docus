# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps
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
        
    Value.objects.filter(column__datasource=datasource.id).delete()
    
    for i, row in enumerate(csv_attach):
        for column in columns:
            value = Value()
            value.value = row[column.csv_index]
            value.data_type = column.data_type
            value.column = column
            value.row = i
            
            if column.data_type == 'point':
                latlng = gmaps.address_to_latlng('%s, cordoba, argentina' %value.value )
                try:
                    point =  MaapPoint(
                        geom=Point(latlng).wkt,
                        name=value.value
                    )
                    point.save()            
                except Exception, e:
                    errors.append(e)
                else:
                    value.point = point
                                        
            value.save()
            
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 


    print errors
