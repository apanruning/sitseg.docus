# -*- coding: utf-8 -*-

from django import forms
from tagging.fields import TagField
from mongoengine.django.auth import User
from models import DataSource, Annotation, Column

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
            ('int','Numero'), 
            ('date','Fecha'), 
            ('point',u'Dirección'),
            ('area','Zona'), 
        ],
        required=False
    )

    class Meta:
        model = Column

ColumnFormSet = forms.formsets.formset_factory(ColumnForm, extra=3)

#class DocumentForm(forms.Form):
#    def __init__(self, data_id, *args, **kwargs):
#        super(DocumentForm, self).__init__(*args, **kwargs)
#        data = DataSource.objects.all()
#
#            self.fields['captcha'] = CaptchaField()

