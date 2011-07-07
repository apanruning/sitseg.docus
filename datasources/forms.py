# -*- coding: utf-8 -*-

from django import forms
from tagging.fields import TagField
from mongoengine.django.auth import User
from mongoforms import MongoForm
from models import DataSource, Annotation, Column

class DataSourceForm(forms.ModelForm):
    name = forms.CharField()
    #attach = forms.FileField(label="Archivo CSV")

    class Meta:
        fields = ('name', 'author','attach')
        model = DataSource
        widgets = {'attach': forms.FileInput}
        
class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation

class ColumnForm(forms.ModelForm):
    data_type = forms.ChoiceField(
        choices=[
            ('str','str'), 
            ('date','date'), 
            ('time','time'),
            ('datetime','datetime'), 
            ('int','int'), 
            ('float','float'), 
            ('dict','dict'), 
            ('point','point')
        ]
    )
    class Meta:
        model = Column

ColumnFormSet = forms.formsets.formset_factory(ColumnForm, extra=3)
    
