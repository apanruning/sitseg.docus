# -*- coding: utf-8 -*-

import os


BASE_DIR = os.path.dirname(__file__)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
   'default' : {
      'ENGINE' : 'django_mongodb_engine',
      'NAME' : 'sitseg',
   }
}

ADMINS = (
    ('tutuca', 'maturburu@gmail.com'),
    ('monetti', 'onetti.martin@gmail.com'),
    ('etnalubma', 'francisco.herrero@gmail.com'),
)

MANAGERS = ADMINS

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Argentina/Cordoba'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-AR'

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'docus.urls'

TEMPLATE_DIRS = (
    'templates',
    os.path.join(BASE_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'datasources',
)

AUTHENTICATION_BACKENDS = ('permission_backend_nonrel.backends.NonrelPermissionBackend',)

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': True,
#    'handlers': {
#        'console':{
#            'level':'DEBUG',
#            'class':'logging.StreamHandler',
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers':['null'],
#            'propagate': True,
#            'level':'INFO',
#        },
#        'django.debug': {
#            'handlers': ['console'],
#            'level': 'INFO',
#        }
#    }
#}


try:
    from local_settings import *
except ImportError:
    pass
