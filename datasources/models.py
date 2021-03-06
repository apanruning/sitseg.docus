# -*- coding: utf-8 -*-

from csv import reader
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from maap.models import MaapPoint, MaapArea
from dateutil.parser import parse as date_parser
from django.template.defaultfilters import slugify
from django import forms
from datetime import datetime

class Annotation(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=50)
    datasource = models.ForeignKey('DataSource')

class Column(models.Model):
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable = False)
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
        
        
class DataSet(models.Model):
    name = models.CharField("Nombre", max_length=50)
    slug = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    author = models.ForeignKey('auth.User')

    @models.permalink
    def get_absolute_url(self):
        return ('dataset_detail',[self.pk])

    def save(self):
        self.slug = slugify(self.name)
        return super(DataSet, self).save()

    def __str__(self):
        return self.name


class DataSource(models.Model):
    name = models.CharField("Nombre",max_length=50)
    slug = models.CharField(max_length=50,editable=False)
    attach = models.FileField("Archivo", upload_to='docs/')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    author = models.ForeignKey('auth.User')
    is_dirty = models.BooleanField(default=True, editable=False)
    dataset = models.ForeignKey('DataSet')
    geopositionated = models.BooleanField(default=False, editable=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ('datasource_detail',[self.pk])

    def __unicode__(self):
        return '%s-%d' %(slugify(self.name), self.id)

    def save(self):
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
        """ assume that the first column has the headers title.
            WARNING: It removes previous columns. Use with care.
        """
        from cStringIO import StringIO
        f = StringIO(self.attach.read())        
        csv_attach = reader(f)
        first_column = csv_attach.next()

        for i, column in enumerate(first_column):
            new_column = Column(name=column,)
            new_column.created = datetime.now()
            new_column.label = slugify(new_column.name)
            new_column.csv_index = i
            new_column.datasource = self 
            new_column.is_available = True
            new_column.save()

class Row(models.Model):
    datasource = models.ForeignKey(DataSource)    
    csv_index = models.IntegerField()


class ValueManager(models.Manager):
    def get_query_set(self):
        return super(ValueManager, self).get_query_set().annotate(
            points=models.Count('point')
        ).order_by('column')

class Value(models.Model):
    column = models.ForeignKey(Column)
    data_type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    point = models.ForeignKey(MaapPoint, null=True, blank=True)
    map_url = models.URLField(null=True, blank=True)
    multiple = models.BooleanField()
    area = models.ForeignKey(MaapArea, null=True)
    row = models.ForeignKey(Row)
    objects = ValueManager()
        
    def __unicode__(self):
        return self.cast_value()
        
    def cast_value(self):
        tests = (
            unicode,
            int,
            float,
            lambda value: date_parser(value)
        )
        
        for test in tests:
            try:
                return test(self.value)
            except ValueError:
                continue
        return self.value

class Out(models.Model):
    text = models.TextField(blank=True)
    session = models.DateTimeField(default=datetime.now(),editable=False) 
    img = models.CharField(max_length=50)
    errors = models.TextField(blank=True)
    
    
__all__ = ['DataSource', 'Column', 'Annotation']
