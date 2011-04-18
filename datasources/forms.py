# -*- coding: utf-8 -*-

from django import forms
from tagging.fields import TagField
from mongoengine.django.auth import User
from models import DataSource

class DataSourceForm(forms.Form):
    name = forms.CharField(label="Nombre")
    attach = forms.FileField(label="Archivo")
    author = forms.ChoiceField(choices=((x.username,x.username) for x in User.objects), label="Autor")
