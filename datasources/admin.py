# -*- coding: utf-8 -*-


from models import DataSource, Column, Annotation
from django.contrib import admin

#class DataSourceAdmin(admin.ModelAdmin):
#    group = 'Data Sources'
#    list_items = ('name', 'created', 'author')

class ColumnAdmin(admin.ModelAdmin):
    model = 'Column'
    list_display = ('name', 'label', 'data_type','is_key')
    list_filter = ('datasource', 'data_type')
    ordering = ('-id',)
    search_fields = ('label','name',)


admin.site.register(DataSource)
admin.site.register(Column,ColumnAdmin)
admin.site.register(Annotation)
