# -*- coding: utf-8 -*-

from django_ztask.decorators import task
from django.conf import settings
from django.forms.models import model_to_dict
from django.template.defaultfilters import slugify
from datasources.models import DataSource
from csv import reader
from StringIO import StringIO
from googlemaps import GoogleMaps


@task()
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
                label = slugify(values['name'])
                params[label] = values
                if values['has_geodata'] and values['geodata_type']=='punto':
                    #TODO manejar otros tipos
                    #TODO Debería tomar un orden de precedencia para los 
                    #      valores geográficos buscar primero el pais, si 
                    #      existe, luego la provincia, luego la ciudad,
                    #      si no existen valores usar `region`
                    local_search = gmaps.local_search('%s %s' %(values['value'], region))

                    
                    if len(local_search['responseData']['results']) == 0:
                        params['map_empty'] = True
                    elif len(local_search['responseData']['results']) > 1:
                        params['map_multiple'] = True
                        params['map_data'] = local_search['responseData']['results']
                    elif len(local_search['responseData']['results']) == 1:
                        result = local_search['responseData']['results'][0]
                        params['map_data'] = result
                        params['map_url'] = result['staticMapUrl']
                        params['lat'] = result['lat']
                        params['lng'] = result['lng']


            except IndexError:
                errors.append('%s has no column "%s"' %(csv_attach,column))
                
        data_collection.insert(params)
    
    if len(errors) == 0:
        datasource.is_dirty = False 
        datasource.save() 
    print columns
    print errors
