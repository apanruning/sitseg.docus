# -*- coding: utf-8 -*-

from datetime import datetime
from django.template.defaultfilters import slugify
from csv import reader
from StringIO import StringIO
from mongoengine import *
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.forms.models import model_to_dict
from googlemaps import GoogleMaps

gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
# datasource Objects

class Annotation(models.Model):

    text = models.TextField()
    author = models.CharField(max_length=50)
    datasource = models.ForeignKey('DataSource')

class Column(models.Model):

    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    # Valid data types are:
    # str, date, time, datetime, int, float, dict, point
    data_type = models.CharField(max_length=50)
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

class Dattum(Document):
    
    def __init__(self,datasource,columns,label):
        self.datasource = datasource
        self.columns = columns
        self.label = label
    
class GeoDattum(Dattum):

    def __init__(self,map_empty=None,map_multiple=None,map_data=None,map_url=None,lat=None,lng=None):
        super(Dattum,self).__init__()
        self.map_empty = map_empty
        self.map_multiple = map_multiple
        self.map_data = map_data
        self.map_url = map_url
        self.lat = lat
        self.lng = lng
       
class DataSource(models.Model):

    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    attach = models.FileField(upload_to="docs")
    created = models.DateTimeField(auto_now_add=True, editable = False)
    author = models.CharField(max_length=50)
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
    
    @property
    def columns_dict(self):
        out = {}
        for column in self.columns:
            out[column.label] = dict(
                name = column.name,
                data_type = column.data_type,
                data_source = self,
                column = column
            )
        return out
        
    @property
    def attach_columns(self):
        """ returns the number of columns for attach """
        csv_attach = reader(StringIO(self.attach.read()))
        first_column = csv.next()
        return len(first_column)

    def import_columns(self):
        """ assume that the first column has the headers title.
            WARNING: It removes previous columns. Use with care.
        """
        csv_attach = reader(StringIO(self.attach.read()))
        first_column = csv_attach.next()
        # Check: Is deleting the previous fields?
        #self.columns = []
        for i, column in enumerate(first_column):
            new_column = Column(name= unicode(column, 'utf-8'), data_type="str")
            new_column.created = datetime.now()
            new_column.label = slugify(new_column.name)
            new_column.csv_index = i
            new_column.datasource = self 
            new_column.is_available=True
            new_column.save()

    def _cast_value(self, data_type, value):
        if (data_type == "float"):
            return float(value)
        if (data_type == "int"):
            return int(value)
        elif (data_type == "str"):
            return value
        else:
            return value

    def _data_collection(self):
        # Check: If database name changes the next will crash
        db = settings.DB
        
        # This create the collection if not exists previously
        data_collection = db['data']    
        return data_collection

    def generate_documents(self, columns=None):
        data_collection = self._data_collection()
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
                'map_empty':False,
                'map_multiple':False,
                'mapa_data':{},
                'map_url':'',
                'lat':0.0,
                'lng':0.0,
            }            
            for column in columns:
                try:
                    dato = GeoDattum()
                    dato.datasource = self.pk
                    values = model_to_dict(column);
                    values['value'] = self._cast_value(
                        column.data_type, 
                        row[column.csv_index]
                    )
                    label = slugify(values['name'])
                    params[label] = values
                    dato.label = values
                    if values['has_geodata'] and values['geodata_type']=='punto':
                        #FIXME usar una señal y mover esta lógica a Column
                        #TODO manejar otros tipos
                        #TODO Debería tomar un orden de precedencia para los 
                        #      valores geográficos buscar primero el pais, si 
                        #      existe, luego la provincia, luego la ciudad,
                        #      si no existen valores usar `region`
                        local_search = gmaps.local_search('%s %s' %(values['value'], region))
                                                
                            
                        if len(local_search['responseData']['results']) == 0:
                            params['map_empty'] = True
                            dato.map_empty = True
                        elif len(local_search['responseData']['results']) > 1:
                            params['map_multiple'] = True
                            params['map_data'] = local_search['responseData']['results']
                            dato.map_multiple = True
                            dato.map_data = local_search['responseData']['results']
                        elif len(local_search['responseData']['results']) == 1:
                            result = local_search['responseData']['results'][0]
                            params['map_data'] = result
                            dato.map_data = result
                            params['map_url'] = result['staticMapUrl']
                            params['lat'] = result['lat']
                            params['lng'] = result['lng']
                            dato.map_url = result['staticMapUrl']
                            dato.lat = result['lat']
                            dato.lng = result['lng']

                        #Aqui se guarda la columna como Document en mongodb

                    dato.save()
                    
                except IndexError:
                    errors.append('{attach} has no column "{column}"'.format({
                        'attach':csv_attach,
                        'column':column,
                    }))
                    
            
            data_collection.insert(params)
        
        if not (len(errors) > 1):
            self.is_dirty = False 
            self.save() 
        
        return {
            'columns':columns,
            'errors':errors
        }
        
        
    def find(self, params={}):
        params.update({"datasource_id": self.id})
        data_collection = self._data_collection()
        return data_collection.find(params)

    
    


__all__ = ['DataSource', 'Column', 'Annotation']
