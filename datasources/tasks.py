# -*- coding: utf-8 -*-

from celery.task import task
from django.conf import settings
from django.forms.models import model_to_dict
from StringIO import StringIO
from csv import reader
from googlemaps import GoogleMaps

from datasources.models import DataSource
from datasources.documents import Dattum
from dateutil.parser import parse as date_parser


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
    #FIXME Usar una cola de tareas
    datasource = DataSource.objects.get(id=datasource)
    region = settings.DEFAULT_REGION
    csv_attach = reader(StringIO(datasource.attach.read()))
    first_column = csv_attach.next() # skip the title column.
    errors = []
    old_dattum = Dattum.objects.filter(datasource_id=datasource.pk)
    old_dattum.delete()
    if columns is not None:
        columns = datasource.column_set.filter(pk__in=columns)
    else:
        columns = datasource.column_set.all()

    for row in csv_attach:
        dato = Dattum(datasource_id=datasource.pk)
        for column in columns:
            try:
                ecol = model_to_dict(column)
                ecol.pop('id')
                ecol['datasource_id'] = datasource.pk
                ecol['value'] = _cast_value(row[column.csv_index])
                ecol['row'] = row.index(row[column.csv_index])
                ecol['column'] = column.name
            except IndexError:
                errors.append('%s has no column "%s"' %(datasource.name,column))
            else:

                if ecol['data_type']=='point':
                    local_search = gmaps.local_search('%s %s' %(ecol['value'], region))
                    results = local_search['responseData']['results']
                    result_len = len(results)
                    ecol['map_multiple'] = []
                    ecol['results'] = []
                    if result_len > 1:

                        for res in results:
                            ecol.map_multiple.append(
                                (
                                    float(result['lat']), 
                                    float(result['lng'])
                                )
                            )
                            ecol.results.append(res)
                    elif result_len == 1:
                        result = results[0]
                        ecol['results'].append(result)
                        ecol['map_url'] = result['staticMapUrl']
                        ecol['point'] = float(result['lat']), float(result['lng'])
            

                dato.columns.append(ecol)
            dato.save()
                
    if len(errors) == 0:
        datasource.has_data = True
        datasource.is_dirty = False 
        datasource.save() 


    print errors
