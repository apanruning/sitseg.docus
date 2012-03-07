# -*- coding: utf-8 -*-

from django import forms
from models import DataSource, Annotation, Column, Value, DataSet
from django.contrib.auth.models import User
from maap.models import MaapArea, MaapPoint

class MaapAreaForm():
    class Meta:
        model = MaapArea

class MaapPointForm():
    class Meta:
        model = MaapPoint

class DataSourceForm(forms.ModelForm):
    author = forms.ModelChoiceField(label='', queryset=User.objects.all(),widget=forms.HiddenInput)
    dataset = forms.ModelChoiceField(label='', queryset=DataSet.objects.all(),widget=forms.HiddenInput)

    class Meta:
        model = DataSource    
        fields = ('attach','name','author','dataset')
        
class ExportForm(forms.Form):
    column_geo = forms.ChoiceField(label='Variable')
    datasource = forms.CharField(widget=forms.HiddenInput)
    name_file = forms.CharField(label='Nombre del Archivo')    

class DataSetForm(forms.ModelForm):
    author = forms.ModelChoiceField(label='', queryset=User.objects.all(),widget=forms.HiddenInput)
    class Meta:
        model = DataSet
        
class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation

class ColumnForm(forms.ModelForm):
    data_type = forms.ChoiceField(
        choices=[
            ('None','---------'), 
            ('point',u'Dirección'),
            ('area',u'Zona'), 
        ],
        required=False
    )
    class Meta:

        model = Column
        
class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        
ColumnFormSet = forms.formsets.formset_factory(ColumnForm, extra=3)
