# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ValueDate.value'
        db.alter_column('datasources_valuedate', 'value', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'ValueDate.value'
        db.alter_column('datasources_valuedate', 'value', self.gf('django.db.models.fields.DateField')())

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datasources.annotation': {
            'Meta': {'object_name': 'Annotation'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.DataSource']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'datasources.column': {
            'Meta': {'ordering': "['csv_index']", 'object_name': 'Column'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'csv_index': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.DataSource']", 'blank': 'True'}),
            'has_geodata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'datasources.dataset': {
            'Meta': {'object_name': 'DataSet'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'datasources.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'attach': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.DataSet']"}),
            'geopositionated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_dirty': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'datasources.out': {
            'Meta': {'object_name': 'Out'},
            'errors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'session': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 9, 2, 0, 0)'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'datasources.row': {
            'Meta': {'object_name': 'Row'},
            'csv_index': ('django.db.models.fields.IntegerField', [], {}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.DataSource']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'datasources.value': {
            'Meta': {'object_name': 'Value'},
            'column': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.Column']"}),
            'data_type': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'row': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.Row']"})
        },
        'datasources.valuearea': {
            'Meta': {'object_name': 'ValueArea', '_ormbases': ['datasources.Value']},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapArea']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datasources.valuebool': {
            'Meta': {'object_name': 'ValueBool', '_ormbases': ['datasources.Value']},
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datasources.valuedate': {
            'Meta': {'object_name': 'ValueDate', '_ormbases': ['datasources.Value']},
            'value': ('django.db.models.fields.DateTimeField', [], {}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datasources.valuefloat': {
            'Meta': {'object_name': 'ValueFloat', '_ormbases': ['datasources.Value']},
            'value': ('django.db.models.fields.FloatField', [], {}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datasources.valueint': {
            'Meta': {'object_name': 'ValueInt', '_ormbases': ['datasources.Value']},
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datasources.valuepoint': {
            'Meta': {'object_name': 'ValuePoint', '_ormbases': ['datasources.Value']},
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapPoint']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datasources.valuetext': {
            'Meta': {'object_name': 'ValueText', '_ormbases': ['datasources.Value']},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapArea']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapPoint']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {}),
            'value_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasources.Value']", 'unique': 'True', 'primary_key': 'True'})
        },
        'maap.icon': {
            'Meta': {'object_name': 'Icon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maap.maaparea': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MaapArea', '_ormbases': ['maap.MaapModel']},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        'maap.maapmodel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MaapModel'},
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        'maap.maappoint': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MaapPoint', '_ormbases': ['maap.MaapModel']},
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.Icon']", 'null': 'True', 'blank': 'True'}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['datasources']