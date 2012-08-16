# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Annotation'
        db.create_table('datasources_annotation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('datasource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.DataSource'])),
        ))
        db.send_create_signal('datasources', ['Annotation'])

        # Adding model 'Column'
        db.create_table('datasources_column', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datasource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.DataSource'])),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('csv_index', self.gf('django.db.models.fields.IntegerField')()),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('has_geodata', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('datasources', ['Column'])

        # Adding model 'DataSet'
        db.create_table('datasources_dataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('datasources', ['DataSet'])

        # Adding model 'DataSource'
        db.create_table('datasources_datasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('attach', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_dirty', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.DataSet'])),
            ('geopositionated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('datasources', ['DataSource'])

        # Adding model 'Row'
        db.create_table('datasources_row', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datasource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.DataSource'])),
            ('csv_index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('datasources', ['Row'])

        # Adding model 'Value'
        db.create_table('datasources_value', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.Column'])),
            ('data_type', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('row', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasources.Row'])),
        ))
        db.send_create_signal('datasources', ['Value'])

        # Adding model 'ValueInt'
        db.create_table('datasources_valueint', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('datasources', ['ValueInt'])

        # Adding model 'ValueText'
        db.create_table('datasources_valuetext', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.MaapArea'], null=True, blank=True)),
            ('point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.MaapPoint'], null=True, blank=True)),
        ))
        db.send_create_signal('datasources', ['ValueText'])

        # Adding model 'ValueFloat'
        db.create_table('datasources_valuefloat', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('datasources', ['ValueFloat'])

        # Adding model 'ValueBool'
        db.create_table('datasources_valuebool', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('datasources', ['ValueBool'])

        # Adding model 'ValueDate'
        db.create_table('datasources_valuedate', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('datasources', ['ValueDate'])

        # Adding model 'ValuePoint'
        db.create_table('datasources_valuepoint', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.MaapPoint'], null=True, blank=True)),
        ))
        db.send_create_signal('datasources', ['ValuePoint'])

        # Adding model 'ValueArea'
        db.create_table('datasources_valuearea', (
            ('value_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasources.Value'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.MaapArea'], null=True, blank=True)),
        ))
        db.send_create_signal('datasources', ['ValueArea'])

        # Adding model 'Out'
        db.create_table('datasources_out', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('session', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 15, 0, 0))),
            ('img', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('errors', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('datasources', ['Out'])


    def backwards(self, orm):
        # Deleting model 'Annotation'
        db.delete_table('datasources_annotation')

        # Deleting model 'Column'
        db.delete_table('datasources_column')

        # Deleting model 'DataSet'
        db.delete_table('datasources_dataset')

        # Deleting model 'DataSource'
        db.delete_table('datasources_datasource')

        # Deleting model 'Row'
        db.delete_table('datasources_row')

        # Deleting model 'Value'
        db.delete_table('datasources_value')

        # Deleting model 'ValueInt'
        db.delete_table('datasources_valueint')

        # Deleting model 'ValueText'
        db.delete_table('datasources_valuetext')

        # Deleting model 'ValueFloat'
        db.delete_table('datasources_valuefloat')

        # Deleting model 'ValueBool'
        db.delete_table('datasources_valuebool')

        # Deleting model 'ValueDate'
        db.delete_table('datasources_valuedate')

        # Deleting model 'ValuePoint'
        db.delete_table('datasources_valuepoint')

        # Deleting model 'ValueArea'
        db.delete_table('datasources_valuearea')

        # Deleting model 'Out'
        db.delete_table('datasources_out')


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
            'csv_index': ('django.db.models.fields.IntegerField', [], {}),
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasources.DataSource']"}),
            'has_geodata': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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
            'session': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 8, 15, 0, 0)'}),
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
            'value': ('django.db.models.fields.DateField', [], {}),
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