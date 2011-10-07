# -*- coding: utf-8 -*-

from django import forms
from tagging.fields import TagField
from mongoengine.django.auth import User
from models import DataSource, Annotation, Column, Value

class DataSourceForm(forms.ModelForm):
    name = forms.CharField()
    #attach = forms.FileField(label="Archivo CSV")

    class Meta:
        fields = ('attach','name', 'author')
        model = DataSource
        widgets = {'attach': forms.FileInput}
        
class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation

class ColumnForm(forms.ModelForm):
    data_type = forms.ChoiceField(
        choices=[
            ('None','---------'), 
            ('str','Texto'), 
            ('float','Flotante'), 
            ('int','Entero'), 
            ('date','Fecha'),
            ('bool','Booleano'),             
            ('point',u'Dirección'),
            ('area','Zona'), 
        ],
        required=False
    )

    class Meta:
        model = Column
        
class ValueForm(forms.ModelForm):

    class Meta:
        model = Value

ColumnFormSet = forms.formsets.formset_factory(ColumnForm, extra=3)
