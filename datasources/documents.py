# -*- coding: utf-8 -*-

from mongoengine import Document, EmbeddedDocument,  fields
import datetime

    
class Dattum(Document):
    datasource_id = fields.IntField(required=True)
    date_modified = fields.DateTimeField(default=datetime.datetime.now)
    columns = fields.ListField(fields.DictField())
    row = fields.IntField()
    value = fields.StringField()
    
