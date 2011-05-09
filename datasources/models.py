# -*- coding: utf-8 -*-

from mongoengine import EmbeddedDocument, Document, fields
from mongoengine.django.auth import User
from datetime import datetime
from django.template.defaultfilters import slugify
from csv import reader
from StringIO import StringIO

class Annotation(EmbeddedDocument):

    text = fields.StringField(required=True)
    author = fields.StringField(required=True)


class Column(EmbeddedDocument):

    name = fields.StringField(required=True)
    # Valid data types are:
    # str, date, time, datetime, int, float, dict, point
    data_type = fields.StringField(required=True)
    is_key = fields.BooleanField(default=False)
    
    
class DataSource(Document):

    name = fields.StringField(required=True)
    slug = fields.StringField(required=True)
    attach = fields.FileField(required=True)
    columns = fields.ListField(fields.EmbeddedDocumentField(Column))
    annotations = fields.ListField(fields.EmbeddedDocumentField(Annotation))
    created = fields.DateTimeField(required=True)
    author = fields.ReferenceField(User, required=True)

    def save(self):
        self.created = datetime.now()
        if self.slug is None:
            slug = slugify(self.name)
            new_slug = slug
            c = 1
            while True:
                try:
                    DataSource.objects.get(slug=new_slug)
                except DataSource.DoesNotExist:
                    break
                else:
                    c += 1
                    new_slug = '%s-%s' % (slug, c)
                    
            self.slug = new_slug

        return super(DataSource, self).save()
    
    @property
    def attach_columns(self):
        """ returns the number of columns for attach """
        csv = reader(StringIO(self.attach.read()))
        first_column = csv.next()
        return len(first_column)

    def import_columns(self):
        """ assume that the first column has the headers title.
            WARNING: It removes previous columns. Use with care.
        """
        csv = reader(StringIO(self.attach.read()))
        first_column = csv.next()
        # Check: Is deleting the previous fields?
        self.columns = []
        for column in first_column:
            new_column = Column(name= unicode(column, 'utf-8'), data_type="str")
            self.columns.append(new_column) 
        self.save()
        
#    def get_absolute_url(self):
#        return reverse('datasources.views.detail', kwargs={'slug': self.slug})


__all__ = ['DataSource', 'Column', 'Annotation']
