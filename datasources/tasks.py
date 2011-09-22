# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps

from datasources.models import DataSource, Value, ValuePoint
from maap.models import MaapPoint
from dateutil.parser import parse as date_parser

from geojson import Point

def _cast_value(value):
    tests = (
        int,
        float,
        lambda value: date_parser(value)
    )
    for test in tests:
        try:
            return test(value)
        except ValueError:
            continue
    return value

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

    for row in csv_attach:
        
        for column in columns:
            if column.data_type == 'point':
                
                try:
                    latlng = ['64', '31']
                    maap_point = MaapPoint(*latlng)
                    point = ValuePoint(column=column, value=maap_point)
                    point.save()
                except Exception, e:
                    errors.append(e)
                
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 


    print errors
