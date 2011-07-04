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
    #def save(self, commit=True):

        #attach = self.files['attach']
        #self.instance.attach.put(
        #    attach.read(),
        #    content_tyle=attach.content_type,
        #    filename=attach.name
        #)

    #    return super(DataSourceForm, self).save(self)

        
class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation

class ColumnForm(forms.ModelForm):
    name = forms.CharField()
    data_type = forms.CharField()
    class Meta:
        fields = ('is_key',)    
        model = Column

ColumnFormSet = forms.formsets.formset_factory(ColumnForm, extra=3)
    
