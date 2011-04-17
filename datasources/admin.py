# -*- coding: utf-8 -*-

import mongoadmin
from models import DataSource


class DataSourceAdmin(mongoadmin.MongoAdmin):
    group = 'Data Sources'
    list_items = ('name', 'created', 'author')


mongoadmin.site.register(DataSource, DataSourceAdmin)
