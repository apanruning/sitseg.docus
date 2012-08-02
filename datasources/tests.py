# -*- coding: utf-8 -*-

from django.test import TestCase
from googlemaps import GoogleMaps
from django.contrib.gis.geos import Point
from maap.models import MaapPoint
from datasources.models import DataSource, Value
from django.conf import settings

class PointFromLatLngTest(TestCase):
    def test_point_from_latlng(self):
        gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
        latlng = gmaps.address_to_latlng(u'Jose javier Diaz 440, cordoba, argentina', )
        point=None
        try:
            point =  MaapPoint(geom=Point(latlng).wkt)
            point.save()            
        except Exception, e:

            self.assertIsNotNone(point, msg=e)
            
class ClasifyPointsTest(TestCase):
    def test_point_from_latlng(self):
        gmaps = GoogleMaps(settings.GOOGLEMAPS_API_KEY)
        latlng = gmaps.address_to_latlng(u'Jose javier Diaz 440, cordoba, argentina', )
        point=None
        try:
            point =  MaapPoint(geom=Point(latlng).wkt)
            point.save()            
        except Exception, e:

            self.assertIsNotNone(point, msg=e)
            

