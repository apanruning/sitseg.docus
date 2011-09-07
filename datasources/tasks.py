# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps
import geojson
from datasources.models import DataSource
from datasources.documents import Dattum, EmbeddedColumn

@task
def generate_documents(datasource, columns=None):
    gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
    #FIXME Usar una cola de tareas
    datasource = DataSource.objects.get(id=datasource)
    region = settings.DEFAULT_REGION
    # Clear previous documents
    data_collection = Dattum.objects.filter(datasource_id=datasource.pk)
    data_collection.delete()
    csv_attach = reader(StringIO(datasource.attach.read()))
    first_column = csv_attach.next() # skip the title column.
    errors = []
    if columns is not None:
        columns = datasource.column_set.filter(pk__in=columns)
    else:
        columns = datasource.column_set.all()

    for row in csv_attach:
        dato = Dattum(datasource_id=datasource.pk)
        for column in columns:
            try:
                col_dict = model_to_dict(column)
                col_dict.pop('id')
                ecol = EmbeddedColumn(**col_dict)
                ecol.value = datasource._cast_value(
                    row[column.csv_index]
                )
            except IndexError:
                errors.append('%s has no column "%s"' %(datasource.name,column))
            else:
                dato.columns.append(ecol)
                if ecol.geodata_type=='punto':
                    #TODO manejar otros tipos
                    #TODO Debería tomar un orden de precedencia para los 
                    #      valores geográficos buscar primero el pais, si 
                    #      existe, luego la provincia, luego la ciudad,
                    #      si no existen valores usar `region`

                    local_search = gmaps.local_search('%s %s' %(ecol.value, region))
                    results = local_search['responseData']['results']
                    result_len = len(results)
                    
                    if result_len > 1:
                        dato.map_multiple = True
                        dato.map_data = results
                    elif result_len == 1:
                        result = results[0]
                        dato.map_staticurl = result['staticMapUrl']
                        #dato.point(result['lat'], result['lng'])
                        dato.geojson = geojson.Point(dato.point)
                
        dato.save()
    
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 

    print 'Creado %s' % dato,
    print '%d columnas' % len(columns),
    print errors
