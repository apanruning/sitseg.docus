# -*- coding: utf-8 -*-

from mongoengine import Document, EmbeddedDocument,  fields
import datetime

    
class Dattum(Document):
    datasource_id = fields.IntField(required=True)
    date_modified = fields.DateTimeField(default=datetime.datetime.now)
    columns = fields.DictField()
    region = fields.StringField()
    has_geodata = fields.BooleanField()
    map_multiple = fields.BooleanField()
