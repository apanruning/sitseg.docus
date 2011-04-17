# -*- coding: utf-8 -*-

from mongoengine import *
from datetime import datetime

class Annotation(EmbeddedDocument):
    created = DateTimeField(required=True)
    text = StringField(required=True)
    author = StringField(required=True)

    def save(self):
        self.created = datetime.now()
        return super(Annotation, self).save()
        
        
class DataSource(Document):

    slug = StringField(required=True)
    name = StringField(required=True)
    attach = FileField(required=True)
    columns = ListField(StringField(required=True))
    annotations = EmbeddedDocumentField(Annotation)
    created = DateTimeField(required=True)
    author = StringField(required=True)
    
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
    
    def get_absolute_url(self):
        return reverse('datasources.views.detail', kwargs={'slug': self.slug})
