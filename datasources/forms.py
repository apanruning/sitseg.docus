# -*- coding: utf-8 -*-

from django import forms
from mongoforms import MongoForm
from models import DataSource


class DataSourceForm(MongoForm):
    class Meta:
        document = DataSource
        fields = ('name', 'attach', 'columns' )
