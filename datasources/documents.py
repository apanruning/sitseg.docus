from mongoengine import Document, EmbeddedDocument,  fields
import datetime

class EmbeddedColumn(EmbeddedDocument):
    created = fields.DateTimeField(default=datetime.datetime.now)

    
class Dattum(Document):
    datasource_id = fields.IntField(required=True)
    date_modified = fields.DateTimeField(default=datetime.datetime.now)
    point = fields.GeoPointField()
    columns = fields.ListField(fields.EmbeddedDocumentField(EmbeddedColumn))
