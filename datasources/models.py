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
    has_geodata = models.NullBooleanField(default=False,)
    is_available = models.NullBooleanField(default=True,)
    class Meta:
        ordering = ['id',]
        
        
class DataSource(models.Model):

    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    attach = models.FileField(upload_to="docs")
    created = models.DateTimeField(auto_now_add=True, editable = False)
    author = models.CharField(max_length=50)

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
        for column in first_column:
            new_column = Column(name= unicode(column, 'utf-8'), data_type="str")
            new_column.created = datetime.now()
            new_column.label = slugify(new_column.name)
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
        db = connect('sitseg')
        
        # This create the collection if not exists previously
        data_collection = db['data']    
        return data_collection

    def generate_documents(self):
        csv_attach = reader(StringIO(self.attach.read()))
        first_column = csv_attach.next() # skip the title column.
        data_collection = self._data_collection()
        
        for row in csv_attach:
            params = {'_datasource_id': self.id}
            columns = self.column_set.all()
            for i, column in enumerate(columns):
                params[column.label] = self._cast_value(
                                                  column.data_type, row[i])
            
            data_collection.insert(params)

    def find(self, params={}):
        params.update({"_datasource_id": self.id})
        data_collection = self._data_collection()
        return data_collection.find(params)
      
#    def get_absolute_url(self):
#        return reverse('datasources.views.detail', kwargs={'slug': self.slug})


__all__ = ['DataSource', 'Column', 'Annotation']
