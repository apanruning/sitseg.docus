# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps

from datasources.models import DataSource
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
    db = settings.DB

    gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
    datasource = DataSource.objects.get(id=datasource)

    region = settings.DEFAULT_REGION

    csv_attach = reader(StringIO(datasource.attach.read()))
    first_column = csv_attach.next() # skip the title column.
    errors = []

    db.dattum.remove({'datasource_id':datasource.pk})
    
    if columns:
        columns = datasource.column_set.filter(pk__in=columns)
    else:
        columns = datasource.column_set.all()

    for row in csv_attach:
        dato = {'datasource_id':datasource.pk}
        for column in columns:
            ecol = model_to_dict(column)
            ecol['value'] = _cast_value(row[column.csv_index])
            ecol.pop('id')
            ecol['name'] = column.name
            dato[column.label] = ecol
            if ecol['data_type'] == 'point':
                try:
                    ecol['point'] = gmaps.address_to_latlng(ecol['value'])
                except Exception, e:
                    errors.append(e)
                            
        db.dattum.insert(dato)
                
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 


    print errors
