# -*- coding: utf-8 -*-

from mongoengine import Document, EmbeddedDocument,  fields
import datetime

    
class Dattum(Document):
    datasource_id = fields.IntField(required=True)
    date_modified = fields.DateTimeField(default=datetime.datetime.now)
    columns = fields.ListField(fields.DictField())
    row = fields.IntField()
    value = fields.StringField()
    
    def _cast_value(self):
        tests = (
            int,
            float,
            lambda value: date_parser(value)
        )
        for test in tests:
            try:
                return test(self.value)
            except ValueError:
                continue
        return self.value
