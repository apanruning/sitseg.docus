# -*- coding: utf-8 -*-

from django import forms
from models import DataSource, Annotation

class DataSourceForm(forms.ModelForm):

    class Meta:
        exclude = ('columns', 'slug')
        model = DataSource


        
class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
