# -*- coding: utf-8 -*-

from datetime import datetime
from django.template.defaultfilters import slugify
from csv import reader
from StringIO import StringIO
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from maap.models import MaapPoint, MaapArea
from dateutil.parser import parse as date_parser


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
    is_available = models.BooleanField(default=True,)
    csv_index = models.IntegerField(editable=False)
    data_type = models.CharField(max_length=50, default='str')
    has_geodata = models.BooleanField(default=False)
    

    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['csv_index',]

    def save(self):
        self.datasource.is_dirty = True
        self.datasource.save()
        if self.data_type in ['point', 'area']:
            self.has_geodata = True

        return super(Column,self).save()
        
        
class DataSource(models.Model):

    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    attach = models.FileField(upload_to="docs")
    created = models.DateTimeField(auto_now_add=True, editable = False)
    author = models.ForeignKey('auth.User')
    #first_import = models.BooleanField(default=True)
    
    is_dirty = models.BooleanField(default=True)
    has_data = models.BooleanField(default=False, editable=False)
    
    def __unicode__(self):
        return self.name

        
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
            new_column = Column(name=unicode(column, 'utf-8'))
            new_column.created = datetime.now()
            new_column.label = slugify(new_column.name)
            new_column.csv_index = i
            new_column.datasource = self 
            new_column.is_available = True
            new_column.save()

class Row(models.Model):
    datasource = models.ForeignKey(DataSource)    
    csv_index = models.IntegerField()


class Value(models.Model):
    column = models.ForeignKey(Column)
    data_type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    point = models.ForeignKey(MaapPoint, null=True)
    area = models.ForeignKey(MaapArea, null=True)
    row = models.ForeignKey(Row)
    
    def cast_value(self):
        tests = (
            int,
            float,
            lambda value: date_parser(value)
        )
        
        for test in tests:
            try:
                return test(self.value)
            except ValueError:
                continue
        return value

__all__ = ['DataSource', 'Column', 'Annotation']
