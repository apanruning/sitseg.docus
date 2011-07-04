# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.contrib.gis.measure import Distance, D
from django.db import models as dbmodels
from django.utils import simplejson
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from settings import DEFAULT_SRID
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

import mptt

from maap.layers import Point, Area, MultiLine, Layer
from django.contrib.gis.gdal import OGRGeometry, SpatialReference

class MaapQuerySet(GeoQuerySet):
    def layer(self):
        elements = self.all()
        objects = []
        for obj in elements:
            objects.append(obj.cast().to_geo_element())
            
        return Layer(elements=objects)

class MaapManager(models.GeoManager):
    def get_query_set(self):
        return MaapQuerySet(self.model)


class MaapModel(models.Model):
    slug = models.SlugField(editable=False, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    creator = models.ForeignKey('auth.User', related_name='created',editable=False) 
    editor = models.ForeignKey('auth.User',related_name='edited', editable=False)
    category = models.ManyToManyField('MaapCategory', null=True, blank=True, related_name='maapmodel_set')
    objects = MaapManager()
        
    class Meta:
        ordering = ('created', 'name',)
    
    @property
    def json_dict(self):
        out = dict(filter(lambda (x,y): not x.startswith('_'), self.__dict__.iteritems()))
        out['created'] = self.created.strftime('%D %T')        
        out['changed'] = self.changed.strftime('%D %T')
        out['absolute_url'] = self.get_absolute_url()
        out['clickable'] = True
        return out

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MaapModel, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        categories = self.category.all()
        if categories:
            cat_slug = categories[0].slug
        else:
            cat_slug = None
        return ('view', [cat_slug, self.id])  

    def to_layer(self):
        # This method only works on inherited models with geom field
        center_point = self.to_geo_element()
        center_point.center = True
        out = get_closest(center_point.geom, self.id).layer()
        out.elements.append(center_point)
        return out

    def cast(self):
        out = self
        try: 
            out = self.maappoint
        except MaapPoint.DoesNotExist:
            pass
        try:
            out = self.maapmultiline
        except MaapMultiLine.DoesNotExist:
            pass
        try:
            out = self.maaparea
        except MaapArea.DoesNotExist:
            pass    
        return out

class MaapCategory(models.Model):
    slug = models.SlugField(unique=True, editable=False)
    name = models.CharField(max_length=35)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    def save(self, *args, **kwargs):        
        if self.id is None:
            num = 0
            while num < 100:
                
                self.slug = slugify(self.name)
                if num > 0:
                    self.slug.append('-%i' % num)
                try:
                    out = super(MaapCategory, self).save( *args, **kwargs)
                    return out
                except:
                    num += 1
        else:
            return super(MaapCategory, self).save(*args, **kwargs)
    
    
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('list_by_category', [self.slug])

class MaapPoint(MaapModel):
   
    geom = models.PointField(srid=DEFAULT_SRID)
    icon = models.ForeignKey('Icon', default=185, blank=True)
    objects = MaapManager()

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        out['icon'] = self.icon.json_dict
        return Point(**out)

    @models.permalink
    def get_absolute_url(self):
        cat_slug = self.category.all()[0].slug
        return ('view',[cat_slug, self.id])
    

class MaapArea(MaapModel):
    objects = MaapManager()

    geom = models.PolygonField(srid=DEFAULT_SRID)

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        return Area(**out)   
        

class MaapMultiLine(MaapModel):
    geom = models.MultiLineStringField(srid = DEFAULT_SRID)
    objects = MaapManager()

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        return MultiLine(**out)
        

class Icon(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = "icons")

    def __unicode__( self ):
        return self.name

    @property
    def json_dict(self):
        out = {}
        out['url'] = self.image.url
        out['width'] = self.image.width
        out['height'] = self.image.height
        return out
        
try: 
    mptt.register(MaapCategory)  
except mptt.AlreadyRegistered:
    pass

