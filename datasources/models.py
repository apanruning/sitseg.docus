# -*- coding: utf-8 -*-

#from mongoengine import EmbeddedDocument, Document, fields
#from mongoengine.django.auth import User
from datetime import datetime
from django.template.defaultfilters import slugify
from csv import reader
from StringIO import StringIO
from mongoengine import connect
from maap.models import MaapModel
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# datasource Objects

class Annotation(models.Model):

    text = models.TextField()
    author = models.CharField(max_length=50)
    datasource = models.ForeignKey('DataSource')

class Column(models.Model):

    name = models.CharField(max_length=50)
    label = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    # Valid data types are:
    # str, date, time, datetime, int, float, dict, point
    data_type = models.CharField(max_length=50)
    is_key = models.NullBooleanField(default=False,)
    datasource = models.ForeignKey('DataSource')
    has_geodata = models.BooleanField(default=False,)
    is_available = models.BooleanField(default=True,)
    csv_index = models.IntegerField()
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
            params = {'datasource_id': self.pk}            
            for column in columns:
                try:
                    params[column.label] = self._cast_value(
                        column.data_type, 
                        row[column.csv_index]
                    )
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
