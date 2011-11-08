# -*- coding: utf-8 -*-

from django import forms
from models import DataSource, Annotation, Column, Value, Workspace, DataSet

class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource    

class WorkspaceForm(forms.ModelForm):
    class Meta:  
        model = Workspace

class DataSetForm(forms.ModelForm):
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
