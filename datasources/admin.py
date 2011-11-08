# -*- coding: utf-8 -*-


from models import DataSource, Column, Annotation, Value, Row, DataSet, Workspace
from django.contrib import admin

#class DataSourceAdmin(admin.ModelAdmin):
#    group = 'Data Sources'
#    list_items = ('name', 'created', 'author')

class ColumnAdmin(admin.ModelAdmin):
    model = 'Column'
    list_display = ('name', 'label', 'is_key')
    list_filter = ('datasource', )
    ordering = ('-id',)
    search_fields = ('label','name')

class DataSetAdmin(admin.ModelAdmin):
    model = DataSet
    list_display = ('name',)
    ordering = ('-id',)
    search_fields = ('name',)

admin.site.register(DataSource)
admin.site.register(Column,ColumnAdmin)
admin.site.register(Annotation)
admin.site.register(Value)
admin.site.register(Row)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(Workspace)
