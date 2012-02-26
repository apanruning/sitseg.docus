from django.contrib.gis import admin
from models import *
from settings import MEDIA_URL
 
class GeoCordobaAdmin(admin.OSMGeoAdmin):
    default_zoom = 10
    map_width = 400
    map_height = 400
    
    extra_js =[MEDIA_URL+'js/OpenStreetMap.js',
               MEDIA_URL+'js/jquery.min.js', 
               MEDIA_URL+'js/tiny_mce/tiny_mce.js',
               MEDIA_URL+'js/tiny_mce/jquery.tinymce.js',
               MEDIA_URL+'js/tiny_mce/textareas.js',]
    
admin.site.register(MaapPoint, GeoCordobaAdmin)
admin.site.register(Icon, GeoCordobaAdmin)
admin.site.register(MaapArea, GeoCordobaAdmin)
admin.site.register(MaapModel)

