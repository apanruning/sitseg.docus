# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from datasources.models import DataSource
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps
import geojson

@task
def generate_documents(datasource, columns=None):
    gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
    #FIXME Usar una cola de tareas
    db = settings.DB
    data_collection = db['data']
    datasource = DataSource.objects.get(id=datasource)
    region = settings.DEFAULT_REGION
    # Clear previous documents
    data_collection.remove({'datasource_id':datasource.pk})
    csv_attach = reader(StringIO(datasource.attach.read()))
    first_column = csv_attach.next() # skip the title column.
    errors = []
    if columns is not None:
        columns = datasource.column_set.filter(pk__in=columns)
    else:
        columns = datasource.column_set.all()

    for row in csv_attach:
        params = {
            'datasource_id': datasource.pk,
            'columns': [],
        }            
        for column in columns:
            try:
                values = model_to_dict(column);
                values['value'] = datasource._cast_value(
                    row[column.csv_index]
                )
            except IndexError:
                errors.append('%s has no column "%s"' %(datasource.name,column))
            else:
                params['columns'].append(values)
                if values['has_geodata'] and values['geodata_type']=='punto':
                    #TODO manejar otros tipos
                    #TODO Debería tomar un orden de precedencia para los 
                    #      valores geográficos buscar primero el pais, si 
                    #      existe, luego la provincia, luego la ciudad,
                    #      si no existen valores usar `region`

                    local_search = gmaps.local_search('%s %s' %(values['value'], region))
                    results = local_search['responseData']['results']
                    result_len = len(results)
                    
                    if result_len == 0:
                        params['map_empty'] = True
                    elif result_len > 1:
                        params['map_multiple'] = True
                        params['map_data'] = results
                    elif result_len == 1:
                        result = results[0]
                        params['map_staticurl'] = result['staticMapUrl']
                        params['geojson'] = geojson.Point(
                            [
                                result['lat'], 
                                result['lng']
                            ]
                        )



                
        data_collection.insert(params)
    
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 
    print columns
    print errors
