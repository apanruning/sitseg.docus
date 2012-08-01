# -*- coding: utf-8 -*-

from models import DataSource, Column, Annotation, Value, Row, DataSet, ValuePoint, ValueArea, ValueText, ValueInt, ValueBool, ValueInt, ValueFloat, ValueDate
from django.contrib import admin

class ColumnAdmin(admin.ModelAdmin):
    model = 'Column'
    list_display = ('name', 'label',)
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
admin.site.register(ValuePoint)
admin.site.register(ValueArea)
admin.site.register(ValueText)
admin.site.register(ValueBool)
admin.site.register(ValueDate)
admin.site.register(ValueFloat)
admin.site.register(ValueInt)
admin.site.register(Row)
admin.site.register(DataSet, DataSetAdmin)

