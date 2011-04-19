# -*- coding: utf-8 -*-
from django.db import models
from djangotoolbox.fields import EmbeddedModelField, ListField
from datetime import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib import admin


class Annotation(models.Model):

    text = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    datasource = models.ForeignKey('DataSource')    

class Column(models.Model):

    name = models.CharField(max_length=1024)
    data_type = models.CharField(max_length=1024)
    is_key = models.BooleanField()
    datasource = models.ForeignKey('DataSource')    
    
class DataSource(models.Model):

    name = models.CharField(max_length=1024)
    slug = models.SlugField(editable=False)
    attach = models.FileField(upload_to='upload')

    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

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
    
    @models.permalink
    def get_absolute_url(self):
        return ('datasources.views.detail', [{'slug': self.slug}])


__all__ = ['DataSource', 'Column', 'Annotation']

class AnnotationAdminInLine(admin.TabularInline):
    model = Annotation
    extra = 1

class ColumnAdminInLine(admin.TabularInline):
    model = Column
    extra = 4

class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'author', 'created')
    list_filter = ('author', 'created')
    inlines = [ColumnAdminInLine, AnnotationAdminInLine]

class ColumnAdmin(admin.ModelAdmin):
    list_filter = ('name', )

class AnnotationAdmin(admin.ModelAdmin):
    list_filter = ('author', )

admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Column, ColumnAdmin)
admin.site.register(Annotation, AnnotationAdmin)
