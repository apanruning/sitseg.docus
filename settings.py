# -*- coding: utf-8 -*-

import os
from mongoengine import connect
import djcelery


POSTGIS_SQL_PATH = '/usr/share/postgresql/8.4/contrib'
TEST_RUNNER='django.contrib.gis.tests.run_tests'


BASE_DIR = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('tutuca', 'maturburu@gmail.com'),
    ('monetti', 'onetti.martin@gmail.com'),
    ('etnalubma', 'francisco.herrero@gmail.com'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.sqlite3',
        'NAME': 'sitseg',
        'USER': '',
        'PASSWORD': '',
        'HOST':'',
        'PORT':''
    }
}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Argentina/Cordoba'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-AR'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

ROOT_URLCONF = 'docus.urls'


MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# Default Space Projection
DEFAULT_SRID = 900913

# Cambiar en local_settings para que apunte al nginx que sirve los archivos
# ej: 'http://gridfs.localhost:9000'

MEDIA_URL = '/media/' 

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    MEDIA_ROOT,
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f@-#g0%bc3prc_71=jzw^jefos5&c(f4oa$dqeovq84i4y@r-f'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    'templates',
    os.path.join(BASE_DIR, 'templates')
)

MIDDLEWARE_CLASSES = (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

CACHES = {
        'default':{
            'BACKEND':'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION':os.path.join(BASE_DIR, 'cache')
         }
}

DEFAULT_REGION = 'Cordoba, Argentina'
PAGINATION_DEFAULT_WINDOW = 2

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'debug_toolbar',
    'pagination',
    'datasources',
    'djcelery',
    'maap',
    'mptt',
    'rpy2',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "localhost",
    "port": 27017,
    "database": "queue",
    "taskmeta_collection": "tasks",
}

BROKER_TRANSPORT = "mongodb"
BROKER_HOST = "localhost"
BROKER_PORT = 27017

# OSM absolute path to csv sources
OSM_CSV_ROOT = os.path.join(os.path.dirname(__file__), 'csv')

try:
    from local_settings import *
except ImportError:
    pass
    
djcelery.setup_loader()
