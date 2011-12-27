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
from maap.models import MaapPoint, MaapArea
from unicodedata import normalize
from django.core.cache import cache
from hashlib import sha1
from djangoosm.utils.words import normalize_street_name

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
        row_obj = Row(
            datasource = datasource,
            csv_index = i,
        )
        row_obj.save()
        for column in columns:
            value = Value()
            value.value = row[column.csv_index]
            value.data_type = column.data_type
            value.column = column
            value.row = row_obj
            value.save()
            
            if column.data_type == 'point':
                hashing = sha1(value.value).hexdigest()
                results = cache.get(hashing)
                if not results:
                    results = gmaps.local_search('%s, cordoba, argentina' %value.value )['responseData']['results']
                    cache.set(hashing,results)

                for result in results:
                    try:
                        latlng = [float(result.get('lat')), float(result.get('lng'))]
                        point =  MaapPoint(
                            geom=Point(latlng).wkt,
                            name=value.value,
                        )
                        map_url = result.get('staticMapUrl', None)
                        point.save()
                        value.point.add(point)
                        value.map_url = map_url 
                        value.save()
                        print point.name 
                    except Exception, e:
                        errors.append(e)

            if column.data_type == 'area':
                try:
                    search_term = normalize_street_name(value.value)
                    barrio = MaapArea.objects.filter(name_norm=search_term) 

                    if len(barrio) == 1:
                        value.area = barrio[0]
                        value.save()
                    print search_term 
                except Exception, e:
                    errors.append(e)
                
                
            
    if len(errors) == 0:
        datasource.is_dirty = False 
        datasource.save() 

    print errors
