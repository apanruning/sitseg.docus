# -*- coding: utf-8 -*-

from datetime import datetime
from django.template.defaultfilters import slugify
from csv import reader
from StringIO import StringIO
from mongoengine import connect
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.forms.models import model_to_dict
from dateutil.parser import parse as date_parser
from googlemaps import GoogleMaps

gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)

class Annotation(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=50)
    datasource = models.ForeignKey('DataSource')

class Column(models.Model):

    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    is_key = models.NullBooleanField(default=False, )
    datasource = models.ForeignKey('DataSource', editable=False)
    has_geodata = models.BooleanField(default=False,)
    is_available = models.BooleanField(default=True,)
    csv_index = models.IntegerField(editable=False)
    geodata_type = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        ordering = ['csv_index',]

    def save(self):
        self.datasource.is_dirty = True
        self.datasource.save()
        return super(Column,self).save()
        
        
class DataSource(models.Model):

    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    attach = models.FileField(upload_to="docs")
    created = models.DateTimeField(auto_now_add=True, editable = False)
    author = models.ForeignKey('auth.User')
    #first_import = models.BooleanField(default=True)
    is_dirty = models.BooleanField(default=True)
    

    def save(self):
        self.created = datetime.now()
        if self.slug is None:
            slug = slugify(self.name)
            new_slug = slug
            c = 1
            while True:
                try:
                    DataSource.objects.get(slug=new_slug)
                except DataSource.DoesNotExist:
                    break
                else:
                    c += 1
                    new_slug = '%s-%s' % (slug, c)
                    
            self.slug = new_slug

        return super(DataSource, self).save()

    def import_columns(self):
        #FIXME Usar una cola de tareas
        """ assume that the first column has the headers title.
            WARNING: It removes previous columns. Use with care.
        """
        csv_attach = reader(StringIO(self.attach.read()))
        first_column = csv_attach.next()
        # Check: Is deleting the previous fields?
        #self.columns = []
        for i, column in enumerate(first_column):
            new_column = Column(name= unicode(column, 'utf-8'))
            new_column.created = datetime.now()
            new_column.label = slugify(new_column.name)
            new_column.csv_index = i
            new_column.datasource = self 
            new_column.is_available=True
            new_column.save()

    def _cast_value(self, value):
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


    def generate_documents(self, columns=None):
        #FIXME Usar una cola de tareas
        db = settings.DB
        data_collection = db['data']
        region = settings.TIME_ZONE.split('/')[-2:] #XXX: debería ir ajustando la región en base a las columnas
        region.reverse()
        region = ', '.join(region)
        # Clear previous documents
        data_collection.remove({'datasource_id':self.pk})
        csv_attach = reader(StringIO(self.attach.read()))
        first_column = csv_attach.next() # skip the title column.
        errors = []
        if columns is not None:
            columns = self.column_set.filter(pk__in=columns)
        else:
            columns = self.column_set.all()

        for row in csv_attach:
            params = {
                'datasource_id': self.pk,
                'columns': [],
            }            
            for column in columns:
                try:
                    values = model_to_dict(column);
                    values['value'] = self._cast_value(
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
            self.is_dirty = False 
            self.save() 
        
        return {
            'columns':columns,
            'errors':errors
        }
        
__all__ = ['DataSource', 'Column', 'Annotation']
