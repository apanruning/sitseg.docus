# -*- coding: utf-8 -*-

from mongoengine import EmbeddedDocument, Document, fields
from mongoengine.django.auth import User
from datetime import datetime
from django.template.defaultfilters import slugify


class Annotation(EmbeddedDocument):

    text = fields.StringField(required=True)
    author = fields.StringField(required=True)


class Column(EmbeddedDocument):

    name = fields.StringField(required=True)
    data_type = fields.StringField(required=True)
    is_key = fields.BooleanField()
    
    
class DataSource(Document):

    name = fields.StringField(required=True)
    slug = fields.StringField(required=True)
    attach = fields.FileField(required=True)
    columns = fields.EmbeddedDocumentField(Column)
    annotations = fields.EmbeddedDocumentField(Annotation)
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
    

#    def get_absolute_url(self):
#        return reverse('datasources.views.detail', kwargs={'slug': self.slug})


__all__ = ['DataSource', 'Column', 'Annotation']
