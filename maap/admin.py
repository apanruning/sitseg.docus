from django.contrib.gis import admin
from django.contrib import admin as simple_admin
from models import *
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import  get_object_or_404
from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django import template
from copy import deepcopy
from settings import MEDIA_URL

class GeoCordobaAdmin(admin.OSMGeoAdmin):
    default_lat = -3686022.8143382
    default_lon = -7145792.0249884
    default_zoom = 10
    map_width = 800
    map_height = 800
    
    extra_js =[MEDIA_URL+'js/OpenStreetMap.js',
               MEDIA_URL+'js/jquery.min.js', 
               MEDIA_URL+'js/tiny_mce/tiny_mce.js',
               MEDIA_URL+'js/tiny_mce/jquery.tinymce.js',
               MEDIA_URL+'js/tiny_mce/textareas.js',]
    
    list_display = ('name','creator','created')           
    list_filter = ('creator','created')
    ordering = ('created','creator')
    search_fields = ('creator','created','creator')

    def save_model(self, request, obj, form, change):

        obj.editor = request.user
        if not change:
            obj.creator = request.user
        obj.save()
        
   
admin.site.register(MaapPoint, GeoCordobaAdmin)
admin.site.register(Icon, admin.GeoModelAdmin)
admin.site.register(MaapArea, GeoCordobaAdmin)

