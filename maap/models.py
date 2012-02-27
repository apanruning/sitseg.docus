# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.utils import simplejson
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from settings import DEFAULT_SRID
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from unicodedata import normalize
from djangoosm.utils.words import normalize_street_name 
from maap.layers import Point, Area, MultiLine, Layer

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
    name = models.CharField(max_length=100, null=True)
    name_norm = models.CharField(max_length=100,null=True,editable=False)
    creator = models.ForeignKey('auth.User',related_name='created',editable=False, null=True) 
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    objects = MaapManager()
        
    class Meta:
        ordering = ('name',)
    
    @property
    def json_dict(self):
        out = dict(filter(lambda (x,y): not x.startswith('_'), self.__dict__.iteritems()))
        return out

    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super(MaapModel, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    def cast(self):
        out = self
        try: 
            out = self.maappoint
        except MaapPoint.DoesNotExist:
            pass
        try:
            out = self.maaparea
        except MaapArea.DoesNotExist:
            pass    
        return out

class MaapPoint(MaapModel):
    geom = models.PointField()
    icon = models.ForeignKey('Icon', blank=True, null=True)
    static_url = models.CharField('Static URL', max_length=500)
    objects = MaapManager()

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        return Point(**out)

    
class MaapArea(MaapModel):
    geom = models.PolygonField(srid=DEFAULT_SRID)
    objects = MaapManager()

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        return Area(**out)   
        

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

