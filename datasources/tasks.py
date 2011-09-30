# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps

from datasources.models import DataSource, Value, Row
from maap.models import MaapPoint

from geojson import Point



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
        row2 = Row()
        row2.datasource = datasource
        row2.csv_index = i
        row2.save()
        for column in columns:
            value = Value()
            value.value = row[column.csv_index]
            value.data_type = column.data_type
            value.column = column
            value.row = row2
            
            if column.data_type == 'point':
                try:
                    latlng = gmaps.address_to_latlng('%s, cordoba, argentina' %value.value, )
                except Exception, e:
                    errors.append(e)
                    
            value.save()
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 


    print errors
