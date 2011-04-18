# -*- coding: utf-8 -*-

from django import forms
from tagging.fields import TagField
from mongoengine.django.auth import User
from mongoforms import MongoForm
from models import DataSource

class DataSourceForm(MongoForm):
    name = forms.CharField()
    attach = forms.FileField(label="Archivo")

    class Meta:
        fields = ('name', 'author')
        document = DataSource

    def save(self, commit=True):

        attach = self.files['attach']
        self.instance.attach.put(
            attach.read(),
            content_tyle=attach.content_type,
            filename=attach.name
        )

        return super(DataSourceForm, self).save(self)

        
class AnnotationForm(forms.Form):

    text = forms.CharField(label=u'Anotación', widget=forms.Textarea)
    author = forms.ChoiceField(choices=((x.username,x.username) for x in User.objects), label="Autor")

